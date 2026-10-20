from __future__ import annotations

"""
投资策略执行情况专题 —— 阶段一 Pipeline V5.0.7

本版本仅负责“源文件数据整理”，不处理 PPT、投决会、宣推材料和比例核查。

处理流程：
1. 读取“产品资料/产品清单.xlsx”中的待核查母产品；
2. 读取“产品资料/子基金策略分类归属.xlsx”，建立子基金代码、一级分类和二级分类映射；
3. 按产品名称匹配“产品资料/产品对应估值表”内的估值表；
4. 动态识别估值表中的“科目代码、科目名称、市价、市值占净值%”表头；
5. 仅处理市价不为空的行，并将科目代码后6位与子基金代码匹配；
6. 汇总同一产品、同一一级分类的净值占比；
7. 同时存在“量化选股”和“指数增强”时，生成“股票多头”；
8. 输出“日报产品比例汇总.xlsx”：
   - 科目比例明细
   - 产品策略分类

重要说明：
- 文件夹内文件均视为已满足日期条件；程序不读取、不比较文件日期。
- “市值占净值%”按普通数值处理，例如 12.3456，不乘以或除以100。
- 估值表列号不固定，程序仅根据表头文字定位列。
- 子基金代码少于6位时直接跳过；达到6位及以上时统一取后6位匹配，程序不补前导0。
- 阶段一只输出“日报产品比例汇总.xlsx”。
"""

import math
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    class _Ansi:
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        RED = "\033[31m"
        RESET_ALL = "\033[0m"

    Fore = _Ansi()  # type: ignore[assignment]
    Style = _Ansi()  # type: ignore[assignment]

    def colorama_init(*, autoreset: bool = True) -> None:
        del autoreset


# ============================================================
# 1. 配置
# ============================================================


@dataclass(frozen=True)
class Config:
    """阶段一的路径、文件名和读取参数。"""

    project_dir: Path = Path(
        r"C:\Users\gyhg-intern\Desktop\投资策略执行情况专题"
    )
    source_dir_name: str = "产品资料"
    product_list_name: str = "产品清单.xlsx"
    strategy_map_name: str = "子基金策略分类归属.xlsx"
    valuation_dir_name: str = "产品对应估值表"
    output_name: str = "日报产品比例汇总.xlsx"

    product_header: str = "产品清单"
    strategy_required_headers: tuple[str, ...] = (
        "子基金代码",
        "子基金全称",
        "一级分类",
        "二级分类",
    )
    valuation_required_headers: tuple[str, ...] = (
        "科目代码",
        "科目名称",
        "市价",
        "市值占净值%",
    )

    valuation_filename_prefix: str = "证券投资基金估值表_"
    valuation_suffixes: tuple[str, ...] = (".xls",)
    valuation_header_scan_rows: int = 120

    # False：按需求不逐行打印“市价为空”和“代码不足6位”的跳过日志。
    verbose_skip_logs: bool = False

    @property
    def source_dir(self) -> Path:
        return self.project_dir / self.source_dir_name

    @property
    def product_list_path(self) -> Path:
        return self.source_dir / self.product_list_name

    @property
    def strategy_map_path(self) -> Path:
        return self.source_dir / self.strategy_map_name

    @property
    def valuation_dir(self) -> Path:
        return self.source_dir / self.valuation_dir_name

    @property
    def output_path(self) -> Path:
        return self.project_dir / self.output_name


CONFIG = Config()

KNOWN_CATEGORY_ORDER = (
    "量化选股",
    "指数增强",
    "股票多头",
    "相对价值",
    "市场中性",
    "固定收益",
    "宏观策略",
    "管理期货",
)

DETAIL_COLUMNS = (
    "产品名称",
    "科目代码",
    "科目名称",
    "科目一级分类",
    "科目二级分类",
    "科目净值占比",
    "产品策略总净值占比",
)

SUMMARY_COLUMNS = (
    "产品名称",
    "一级分类",
    "总净值占比",
)


# ============================================================
# 2. 日志与统计
# ============================================================


class LogLevel:
    DEFAULT = "default"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Logger:
    def __init__(self) -> None:
        colorama_init(autoreset=True)

    @staticmethod
    def _color(level: str) -> str:
        return {
            LogLevel.SUCCESS: Fore.GREEN,
            LogLevel.WARNING: Fore.YELLOW,
            LogLevel.ERROR: Fore.RED,
        }.get(level, "")

    def log(
        self,
        stage: str,
        *,
        product: Any = "N/A",
        item: Any = "N/A",
        file: Any = "N/A",
        status: str,
        level: str = LogLevel.DEFAULT,
    ) -> None:
        product_text = clean_display_value(product)
        item_text = clean_display_value(item)
        file_text = clean_display_value(file)
        message = (
            f"[{stage}] 产品：{product_text} | 科目/策略：{item_text} | "
            f"文件：{file_text} | 状态：{status}"
        )
        color = self._color(level)
        if color:
            print(f"{color}{message}{Style.RESET_ALL}")
        else:
            print(message)

    def candidate(self, filename: str) -> None:
        print(f"{Fore.YELLOW}候选文件：{filename}{Style.RESET_ALL}")


@dataclass
class Stats:
    product_count: int = 0
    valuation_matched_products: int = 0
    valuation_missing_products: int = 0
    valuation_ambiguous_products: int = 0
    valuation_read_failed_products: int = 0

    valuation_rows_scanned: int = 0
    price_blank_rows: int = 0
    short_code_rows: int = 0
    code_match_success: int = 0
    code_match_failed: int = 0
    code_conflict_rows: int = 0
    ratio_parse_failed: int = 0

    valid_detail_rows: int = 0
    strategy_summary_rows: int = 0
    stock_long_rows: int = 0


class PipelineFatalError(RuntimeError):
    def __init__(self, stage: str, file: str, reason: str) -> None:
        super().__init__(reason)
        self.stage = stage
        self.file = file
        self.reason = reason


@dataclass(frozen=True)
class StrategyRecord:
    code: str
    fund_name: str
    primary_category: str
    secondary_category: str = ""


@dataclass
class StrategyMapping:
    records: dict[str, StrategyRecord] = field(default_factory=dict)
    conflicts: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class ValuationMatch:
    status: str  # matched / missing / ambiguous
    selected: Optional[Path] = None
    candidates: tuple[Path, ...] = ()


@dataclass(frozen=True)
class HeaderLocation:
    sheet_name: str
    header_row_zero_based: int
    column_positions: dict[str, int]


# ============================================================
# 3. 通用清洗函数
# ============================================================


_SPACE_RE = re.compile(r"\s+")
_NON_ALNUM_CN_RE = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass
    return isinstance(value, str) and value.strip() == ""


def clean_display_value(value: Any) -> str:
    if is_blank(value):
        return "N/A"
    return str(value).strip().replace("\r", " ").replace("\n", " ")


def normalize_header(value: Any) -> str:
    if is_blank(value):
        return ""
    text = str(value).strip()
    text = text.replace("％", "%").replace("：", ":")
    text = _SPACE_RE.sub("", text)
    return text


def normalize_name(value: Any) -> str:
    """用于产品名和文件名匹配，不改变最终输出名称。"""
    if is_blank(value):
        return ""
    text = str(value).strip().lower()
    text = text.replace("（", "(").replace("）", ")")
    return _NON_ALNUM_CN_RE.sub("", text)


def excel_scalar_to_text(value: Any) -> str:
    """尽量将Excel数值代码恢复为不带“.0”的文本。"""
    if is_blank(value):
        return ""

    if isinstance(value, bool):
        return str(value)

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        if value.is_integer():
            return str(int(value))
        # 对科学计数法尽可能展开；代码字段通常不应有小数部分。
        return format(value, ".15g")

    text = str(value).strip()
    if re.fullmatch(r"[+-]?\d+\.0+", text):
        return text.split(".", 1)[0]
    return text


def normalize_code_text(value: Any) -> str:
    """
    规范基金代码，但保留英文字母。

    私募基金代码可能是 ``SVS398`` 这类6位字母数字组合，不能只提取数字。
    本函数执行：
    1. Excel标量转文本；
    2. Unicode全角字符转半角；
    3. 转为大写；
    4. 仅保留A-Z和0-9。
    """
    text = excel_scalar_to_text(value)
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text).upper()
    return "".join(re.findall(r"[A-Z0-9]", text))


def normalize_strategy_code(value: Any) -> str:
    """
    将策略分类表中的子基金代码用于后6位匹配。

    - 少于6位：直接跳过；
    - 等于6位：原样保留；
    - 超过6位：取后6位；
    - 不补前导0。
    """
    code = normalize_code_text(value)
    if len(code) < 6:
        return ""
    return code[-6:]


def extract_subject_code(value: Any) -> tuple[str, str]:
    """
    返回：(原始科目代码文本, 后6位字母数字代码)。

    按需求，估值表科目代码规范化后不足6位时直接跳过。
    """
    raw_text = excel_scalar_to_text(value)
    code = normalize_code_text(value)
    if len(code) < 6:
        return raw_text, ""
    return raw_text, code[-6:]


def parse_plain_number(value: Any) -> Optional[float]:
    """解析普通数字；不进行百分比倍率换算。"""
    if is_blank(value):
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        number = float(value)
        return number if math.isfinite(number) else None

    text = str(value).strip()
    text = text.replace(",", "").replace("，", "")
    text = text.replace("％", "%")
    # 数据定义为普通数字；若源单元格意外带百分号，仅去符号，不改变倍率。
    text = text.rstrip("%").strip()
    if text in {"", "-", "--", "—", "N/A", "n/a", "NA", "na"}:
        return None

    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def excel_engine(path: Path) -> Optional[str]:
    suffix = path.suffix.lower()
    if suffix == ".xls":
        return "xlrd"
    if suffix in {".xlsx", ".xlsm"}:
        return "openpyxl"
    return None


def friendly_excel_error(exc: Exception) -> str:
    message = str(exc).strip() or exc.__class__.__name__
    lowered = message.lower()
    if "xlrd" in lowered:
        return "缺少xlrd依赖，请运行：pip install xlrd>=2.0.1"
    if "permission" in lowered or "denied" in lowered:
        return "没有文件访问权限，或文件正被其他程序占用"
    return message


# ============================================================
# 4. 输入文件读取
# ============================================================


def ensure_inputs(config: Config, logger: Logger) -> list[Path]:
    """检查必要输入，并返回估值表文件列表。"""
    required_files = (
        config.product_list_path,
        config.strategy_map_path,
    )

    for path in required_files:
        if not path.exists():
            logger.log(
                "文件扫描",
                file=path.name,
                status="未找到文件",
                level=LogLevel.ERROR,
            )
            raise PipelineFatalError("文件扫描", str(path), "未找到必要输入文件")
        logger.log(
            "文件扫描",
            file=path.name,
            status="文件读取成功",
            level=LogLevel.SUCCESS,
        )

    if not config.valuation_dir.exists() or not config.valuation_dir.is_dir():
        logger.log(
            "文件扫描",
            file=config.valuation_dir_name,
            status="未找到估值表目录",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError(
            "文件扫描", str(config.valuation_dir), "未找到估值表目录"
        )

    suffixes = {suffix.lower() for suffix in config.valuation_suffixes}
    valuation_files = sorted(
        (
            path
            for path in config.valuation_dir.iterdir()
            if path.is_file()
            and not path.name.startswith("~$")
            and path.suffix.lower() in suffixes
        ),
        key=lambda path: path.name.lower(),
    )

    if not valuation_files:
        logger.log(
            "文件扫描",
            file=config.valuation_dir_name,
            status="未找到XLS估值表",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError(
            "文件扫描", str(config.valuation_dir), "未找到XLS估值表"
        )

    logger.log(
        "文件扫描",
        file=config.valuation_dir_name,
        status=f"找到{len(valuation_files)}个XLS估值表",
        level=LogLevel.SUCCESS,
    )
    return valuation_files


def find_sheet_with_headers(
    workbook_path: Path,
    required_headers: Iterable[str],
    *,
    fixed_header_row_zero_based: Optional[int] = None,
    scan_rows: int = 50,
) -> tuple[str, pd.DataFrame, int, dict[str, int]]:
    """在工作簿中找到包含指定表头的工作表。"""
    required = tuple(normalize_header(header) for header in required_headers)
    engine = excel_engine(workbook_path)

    try:
        excel_file = pd.ExcelFile(workbook_path, engine=engine)
    except Exception as exc:
        raise RuntimeError(friendly_excel_error(exc)) from exc

    for sheet_name in excel_file.sheet_names:
        try:
            preview = pd.read_excel(
                excel_file,
                sheet_name=sheet_name,
                header=None,
                dtype=object,
            )
        except Exception as exc:
            raise RuntimeError(friendly_excel_error(exc)) from exc

        if preview.empty:
            continue

        if fixed_header_row_zero_based is None:
            row_candidates = range(min(scan_rows, len(preview.index)))
        else:
            row_candidates = (fixed_header_row_zero_based,)

        for row_index in row_candidates:
            if row_index < 0 or row_index >= len(preview.index):
                continue
            row_values = [normalize_header(value) for value in preview.iloc[row_index].tolist()]
            positions: dict[str, int] = {}
            for header in required:
                try:
                    positions[header] = row_values.index(header)
                except ValueError:
                    break
            if len(positions) == len(required):
                original_positions = {
                    original: positions[normalize_header(original)]
                    for original in required_headers
                }
                return sheet_name, preview, row_index, original_positions

    raise KeyError("/".join(required_headers))


def read_product_list(
    config: Config,
    logger: Logger,
) -> list[str]:
    try:
        sheet_name, frame, header_row, positions = find_sheet_with_headers(
            config.product_list_path,
            (config.product_header,),
            fixed_header_row_zero_based=0,
        )
    except KeyError as exc:
        logger.log(
            "文件扫描",
            file=config.product_list_name,
            status="未找到“产品清单”表头",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError(
            "产品读取", str(config.product_list_path), "未找到“产品清单”表头"
        ) from exc
    except Exception as exc:
        raise PipelineFatalError(
            "产品读取", str(config.product_list_path), str(exc)
        ) from exc

    del sheet_name, header_row
    product_col = positions[config.product_header]

    products: list[str] = []
    seen: set[str] = set()
    for value in frame.iloc[1:, product_col].tolist():
        if is_blank(value):
            # pandas一般不会保留工作表末尾空行；中间空行按规则正常跳过。
            logger.log(
                "产品读取",
                file=config.product_list_name,
                status="产品名称为空，已跳过",
                level=LogLevel.DEFAULT,
            )
            continue

        product = str(value).strip()
        key = normalize_name(product)
        if not key:
            continue

        if key in seen:
            logger.log(
                "产品读取",
                product=product,
                file=config.product_list_name,
                status="产品名称重复，已按单一产品处理",
                level=LogLevel.WARNING,
            )
            continue

        seen.add(key)
        products.append(product)
        logger.log(
            "产品读取",
            product=product,
            file=config.product_list_name,
            status="产品读取成功",
            level=LogLevel.SUCCESS,
        )

    if not products:
        raise PipelineFatalError(
            "产品读取", str(config.product_list_path), "产品清单中没有有效产品"
        )

    logger.log(
        "产品读取",
        file=config.product_list_name,
        status=f"共读取{len(products)}个待核查产品",
        level=LogLevel.SUCCESS,
    )
    return products


def read_strategy_mapping(
    config: Config,
    logger: Logger,
) -> StrategyMapping:
    required_headers = config.strategy_required_headers

    try:
        sheet_name, frame, header_row, positions = find_sheet_with_headers(
            config.strategy_map_path,
            required_headers,
            fixed_header_row_zero_based=0,
        )
    except KeyError as exc:
        missing_text = "/".join(required_headers)
        logger.log(
            "文件扫描",
            file=config.strategy_map_name,
            status=f"缺少必要表头：{missing_text}",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError(
            "策略分类", str(config.strategy_map_path), f"缺少必要表头：{missing_text}"
        ) from exc
    except Exception as exc:
        raise PipelineFatalError(
            "策略分类", str(config.strategy_map_path), str(exc)
        ) from exc

    del sheet_name

    candidates: dict[str, list[StrategyRecord]] = {}
    for _, row in frame.iloc[header_row + 1 :].iterrows():
        code = normalize_strategy_code(row.iloc[positions["子基金代码"]])
        fund_name = clean_display_value(row.iloc[positions["子基金全称"]])
        category = clean_display_value(row.iloc[positions["一级分类"]])
        secondary = clean_display_value(row.iloc[positions["二级分类"]])
        if secondary == "N/A":
            secondary = ""

        if not code or fund_name == "N/A" or category == "N/A":
            continue

        record = StrategyRecord(
            code=code,
            fund_name=fund_name,
            primary_category=category,
            secondary_category=secondary,
        )
        candidates.setdefault(code, []).append(record)

    mapping = StrategyMapping()
    for code, records in candidates.items():
        categories = sorted({record.primary_category for record in records})
        if len(categories) > 1:
            mapping.conflicts[code] = tuple(categories)
            logger.log(
                "文件扫描",
                item=code,
                file=config.strategy_map_name,
                status="同一子基金代码存在多个一级分类，需人工确认",
                level=LogLevel.WARNING,
            )
            continue
        mapping.records[code] = records[0]

    if not mapping.records:
        logger.log(
            "文件扫描",
            file=config.strategy_map_name,
            status="未生成任何有效子基金策略映射，请检查子基金代码格式",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError(
            "策略分类",
            str(config.strategy_map_path),
            "未生成任何有效子基金策略映射",
        )

    sample_codes = "、".join(list(mapping.records.keys())[:5])
    logger.log(
        "文件扫描",
        file=config.strategy_map_name,
        status=(
            f"读取{len(mapping.records)}条有效子基金策略映射"
            + (f"；代码示例：{sample_codes}" if sample_codes else "")
        ),
        level=LogLevel.SUCCESS,
    )
    return mapping


# ============================================================
# 5. 估值表匹配与提取
# ============================================================


def product_name_from_valuation_filename(path: Path, config: Config) -> str:
    """
    从“证券投资基金估值表_[产品名称]_[任意后缀].xls”取产品名称部分。
    只剥离最后一个下划线后的尾部，不解析、不判断该尾部是否为日期。
    """
    stem = path.stem
    prefix = config.valuation_filename_prefix
    if not stem.startswith(prefix):
        return ""
    payload = stem[len(prefix) :]
    if "_" not in payload:
        return payload.strip()
    product_part, _ignored_tail = payload.rsplit("_", 1)
    return product_part.strip()


def build_valuation_index(
    files: Iterable[Path],
    config: Config,
) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in files:
        product_part = product_name_from_valuation_filename(path, config)
        normalized = normalize_name(product_part)
        if normalized:
            index.setdefault(normalized, []).append(path)
    return index


def match_valuation_file(
    product: str,
    valuation_files: list[Path],
    valuation_index: dict[str, list[Path]],
    config: Config,
) -> ValuationMatch:
    product_key = normalize_name(product)
    exact_candidates = valuation_index.get(product_key, [])

    if len(exact_candidates) == 1:
        return ValuationMatch("matched", exact_candidates[0], tuple(exact_candidates))
    if len(exact_candidates) > 1:
        return ValuationMatch("ambiguous", None, tuple(exact_candidates))

    # 文件若未严格遵循模板，仍允许在剥离日期尾部后进行规范化精确匹配。
    fallback_candidates: list[Path] = []
    for path in valuation_files:
        extracted = product_name_from_valuation_filename(path, config)
        if normalize_name(extracted) == product_key:
            fallback_candidates.append(path)

    if len(fallback_candidates) == 1:
        return ValuationMatch("matched", fallback_candidates[0], tuple(fallback_candidates))
    if len(fallback_candidates) > 1:
        return ValuationMatch("ambiguous", None, tuple(fallback_candidates))
    return ValuationMatch("missing")


def locate_valuation_header(
    path: Path,
    config: Config,
) -> tuple[HeaderLocation, pd.DataFrame]:
    try:
        sheet_name, frame, header_row, positions = find_sheet_with_headers(
            path,
            config.valuation_required_headers,
            fixed_header_row_zero_based=None,
            scan_rows=config.valuation_header_scan_rows,
        )
    except KeyError as exc:
        raise KeyError("未找到完整估值表表头") from exc
    return HeaderLocation(sheet_name, header_row, positions), frame


def process_valuation_file(
    *,
    product: str,
    path: Path,
    mapping: StrategyMapping,
    config: Config,
    logger: Logger,
    stats: Stats,
) -> list[dict[str, Any]]:
    logger.log(
        "估值表读取",
        product=product,
        file=path.name,
        status="开始读取估值表",
        level=LogLevel.DEFAULT,
    )

    try:
        location, frame = locate_valuation_header(path, config)
    except KeyError:
        logger.log(
            "估值表读取",
            product=product,
            file=path.name,
            status="未找到完整估值表表头",
            level=LogLevel.ERROR,
        )
        stats.valuation_read_failed_products += 1
        return []
    except Exception as exc:
        logger.log(
            "估值表读取",
            product=product,
            file=path.name,
            status=f"文件读取失败：{friendly_excel_error(exc)}",
            level=LogLevel.ERROR,
        )
        stats.valuation_read_failed_products += 1
        return []

    logger.log(
        "估值表读取",
        product=product,
        file=path.name,
        status=(
            f"识别到表头，工作表“{location.sheet_name}”第"
            f"{location.header_row_zero_based + 1}行"
        ),
        level=LogLevel.SUCCESS,
    )

    positions = location.column_positions
    data_frame = frame.iloc[location.header_row_zero_based + 1 :]

    local_scanned = 0
    local_success = 0
    local_price_blank = 0
    local_short_code = 0
    local_unmatched = 0
    detail_rows: list[dict[str, Any]] = []

    for _, row in data_frame.iterrows():
        local_scanned += 1
        stats.valuation_rows_scanned += 1

        market_price = row.iloc[positions["市价"]]
        if is_blank(market_price):
            local_price_blank += 1
            stats.price_blank_rows += 1
            if config.verbose_skip_logs:
                logger.log(
                    "估值提取",
                    product=product,
                    item=row.iloc[positions["科目名称"]],
                    file=path.name,
                    status="市价为空，已跳过",
                    level=LogLevel.DEFAULT,
                )
            continue

        raw_code, code6 = extract_subject_code(row.iloc[positions["科目代码"]])
        subject_name = clean_display_value(row.iloc[positions["科目名称"]])
        if not code6:
            local_short_code += 1
            stats.short_code_rows += 1
            if config.verbose_skip_logs:
                logger.log(
                    "估值提取",
                    product=product,
                    item=subject_name,
                    file=path.name,
                    status="科目代码不足6位，已跳过",
                    level=LogLevel.DEFAULT,
                )
            continue

        if code6 in mapping.conflicts:
            local_unmatched += 1
            stats.code_conflict_rows += 1
            logger.log(
                "策略匹配",
                product=product,
                item=subject_name,
                file=config.strategy_map_name,
                status=(
                    f"代码后6位{code6}在策略表中存在分类冲突，需人工确认"
                ),
                level=LogLevel.WARNING,
            )
            continue

        strategy = mapping.records.get(code6)
        if strategy is None:
            local_unmatched += 1
            stats.code_match_failed += 1
            logger.log(
                "策略匹配",
                product=product,
                item=subject_name,
                file=config.strategy_map_name,
                status=(f"原科目代码{raw_code}，规范化后6位{code6}未找到策略分类，需人工确认"),
                level=LogLevel.WARNING,
            )
            continue

        stats.code_match_success += 1
        logger.log(
            "策略匹配",
            product=product,
            item=subject_name,
            file=config.strategy_map_name,
            status=(
                f"代码后6位{code6}匹配成功，一级分类为"
                f"{strategy.primary_category}"
            ),
            level=LogLevel.SUCCESS,
        )

        ratio_raw = row.iloc[positions["市值占净值%"]]
        ratio = parse_plain_number(ratio_raw)
        if ratio is None:
            stats.ratio_parse_failed += 1
            logger.log(
                "估值提取",
                product=product,
                item=subject_name,
                file=path.name,
                status="市值占净值%无法转换为数字",
                level=LogLevel.ERROR,
            )
            continue

        local_success += 1
        logger.log(
            "估值提取",
            product=product,
            item=subject_name,
            file=path.name,
            status=f"净值占比提取成功：{ratio:.4f}",
            level=LogLevel.SUCCESS,
        )

        detail_rows.append(
            {
                "产品名称": product,
                "科目代码": raw_code,
                "科目名称": subject_name,
                "科目一级分类": strategy.primary_category,
                "科目二级分类": strategy.secondary_category,
                "科目净值占比": float(ratio),
            }
        )

    summary_status = (
        f"扫描{local_scanned}行，成功提取{local_success}行，"
        f"市价为空跳过{local_price_blank}行，代码不足6位跳过"
        f"{local_short_code}行，策略未匹配{local_unmatched}行"
    )
    logger.log(
        "估值提取",
        product=product,
        file=path.name,
        status=summary_status,
        level=LogLevel.SUCCESS if local_success > 0 else LogLevel.ERROR,
    )

    if not detail_rows:
        logger.log(
            "估值提取",
            product=product,
            file=path.name,
            status="未提取到有效子基金科目",
            level=LogLevel.ERROR,
        )

    return detail_rows


# ============================================================
# 6. 汇总与输出
# ============================================================


def category_sort_key(category: str) -> tuple[int, str]:
    try:
        return KNOWN_CATEGORY_ORDER.index(category), category
    except ValueError:
        return len(KNOWN_CATEGORY_ORDER), category


def build_outputs(
    detail_rows: list[dict[str, Any]],
    products: list[str],
    config: Config,
    logger: Logger,
    stats: Stats,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if detail_rows:
        detail = pd.DataFrame(detail_rows)
        detail["科目净值占比"] = pd.to_numeric(
            detail["科目净值占比"], errors="coerce"
        )

        totals = (
            detail.groupby(["产品名称", "科目一级分类"], sort=False)["科目净值占比"]
            .sum(min_count=1)
            .round(4)
        )
        detail["产品策略总净值占比"] = [
            totals.get((product, category), math.nan)
            for product, category in zip(
                detail["产品名称"], detail["科目一级分类"]
            )
        ]
        detail["科目净值占比"] = detail["科目净值占比"].round(4)
        detail["产品策略总净值占比"] = detail[
            "产品策略总净值占比"
        ].round(4)
    else:
        detail = pd.DataFrame(columns=DETAIL_COLUMNS)
        totals = pd.Series(dtype=float)

    product_order = {product: index for index, product in enumerate(products)}
    summary_rows: list[dict[str, Any]] = []
    stock_long_detail_rows: dict[str, dict[str, Any]] = {}

    if not totals.empty:
        grouped_items = list(totals.items())
        grouped_items.sort(
            key=lambda item: (
                product_order.get(item[0][0], len(product_order)),
                category_sort_key(str(item[0][1])),
            )
        )

        product_category_values: dict[str, dict[str, float]] = {}
        for (product, category), total in grouped_items:
            total_value = round(float(total), 4)
            product_category_values.setdefault(product, {})[str(category)] = total_value
            summary_rows.append(
                {
                    "产品名称": product,
                    "一级分类": category,
                    "总净值占比": total_value,
                }
            )
            logger.log(
                "策略汇总",
                product=product,
                item=category,
                file=config.output_name,
                status=f"总净值占比为{total_value:.4f}",
                level=LogLevel.SUCCESS,
            )

        stock_long_rows: list[dict[str, Any]] = []
        for product in products:
            category_values = product_category_values.get(product, {})
            if "量化选股" in category_values and "指数增强" in category_values:
                quant = category_values["量化选股"]
                index_enhancement = category_values["指数增强"]
                stock_long = round(quant + index_enhancement, 4)
                stock_long_rows.append(
                    {
                        "产品名称": product,
                        "一级分类": "股票多头",
                        "总净值占比": stock_long,
                    }
                )
                stock_long_detail_rows[product] = {
                    "产品名称": product,
                    "科目代码": "",
                    "科目名称": "",
                    "科目一级分类": "股票多头",
                    "科目二级分类": "",
                    "科目净值占比": math.nan,
                    "产品策略总净值占比": stock_long,
                }
                stats.stock_long_rows += 1
                logger.log(
                    "股票多头",
                    product=product,
                    item="股票多头",
                    file=config.output_name,
                    status=(
                        f"量化选股{quant:.4f} + 指数增强"
                        f"{index_enhancement:.4f} = {stock_long:.4f}"
                    ),
                    level=LogLevel.SUCCESS,
                )

        summary_rows.extend(stock_long_rows)
        summary_rows.sort(
            key=lambda row: (
                product_order.get(row["产品名称"], len(product_order)),
                category_sort_key(str(row["一级分类"])),
            )
        )

    summary = pd.DataFrame(summary_rows, columns=SUMMARY_COLUMNS)

    if stock_long_detail_rows and not detail.empty:
        original_rows = detail.to_dict("records")
        last_position_by_product: dict[str, int] = {}
        for position, row in enumerate(original_rows):
            last_position_by_product[str(row["产品名称"])] = position

        detail_with_stock_long: list[dict[str, Any]] = []
        for position, row in enumerate(original_rows):
            detail_with_stock_long.append(row)
            product = str(row["产品名称"])
            if (
                last_position_by_product.get(product) == position
                and product in stock_long_detail_rows
            ):
                detail_with_stock_long.append(stock_long_detail_rows[product])

        detail = pd.DataFrame(detail_with_stock_long)

    detail = detail.reindex(columns=DETAIL_COLUMNS)

    stats.valid_detail_rows = len(detail.index)
    stats.strategy_summary_rows = len(summary.index)
    return detail, summary


def style_output_workbook(path: Path) -> None:
    workbook = load_workbook(path)

    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    thin_gray = Side(style="thin", color="D9E2F3")
    border = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)

    widths: dict[str, tuple[float, ...]] = {
        "科目比例明细": (38, 22, 42, 18, 22, 18, 22),
        "产品策略分类": (38, 18, 18),
    }

    for worksheet in workbook.worksheets:
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        worksheet.sheet_view.showGridLines = False
        worksheet.row_dimensions[1].height = 24

        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = border

        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                cell.border = border
                cell.alignment = Alignment(vertical="center", wrap_text=False)

        sheet_widths = widths.get(worksheet.title, ())
        for column_index in range(1, worksheet.max_column + 1):
            width = (
                sheet_widths[column_index - 1]
                if column_index <= len(sheet_widths)
                else 18
            )
            worksheet.column_dimensions[get_column_letter(column_index)].width = width

        if worksheet.title == "科目比例明细":
            for cell in worksheet["B"][1:]:
                cell.number_format = "@"
            for column in ("F", "G"):
                for cell in worksheet[column][1:]:
                    cell.number_format = "0.0000"
                    cell.alignment = Alignment(horizontal="right", vertical="center")
            for column in ("B", "D", "E"):
                for cell in worksheet[column][1:]:
                    cell.alignment = Alignment(horizontal="center", vertical="center")

        if worksheet.title == "产品策略分类":
            for cell in worksheet["B"][1:]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            for cell in worksheet["C"][1:]:
                cell.number_format = "0.0000"
                cell.alignment = Alignment(horizontal="right", vertical="center")

        worksheet.auto_filter.ref = f"A1:{get_column_letter(worksheet.max_column)}{worksheet.max_row}"

    workbook.save(path)


def write_output(
    detail: pd.DataFrame,
    summary: pd.DataFrame,
    config: Config,
    logger: Logger,
) -> None:
    output_path = config.output_path
    temp_path = output_path.with_name(f".{output_path.stem}.tmp{output_path.suffix}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if temp_path.exists():
            temp_path.unlink()

        with pd.ExcelWriter(temp_path, engine="openpyxl") as writer:
            detail.to_excel(writer, sheet_name="科目比例明细", index=False)
            summary.to_excel(writer, sheet_name="产品策略分类", index=False)

        style_output_workbook(temp_path)
        os.replace(temp_path, output_path)
    except PermissionError as exc:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        logger.log(
            "文件输出",
            file=config.output_name,
            status="保存失败：文件可能正在被Excel占用",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError(
            "文件输出", str(output_path), "文件可能正在被Excel占用"
        ) from exc
    except Exception as exc:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        logger.log(
            "文件输出",
            file=config.output_name,
            status=f"保存失败：{exc}",
            level=LogLevel.ERROR,
        )
        raise PipelineFatalError("文件输出", str(output_path), str(exc)) from exc

    logger.log(
        "文件输出",
        file=config.output_name,
        status="保存成功",
        level=LogLevel.SUCCESS,
    )


# ============================================================
# 7. 运行入口
# ============================================================


def print_startup(config: Config) -> None:
    print("================ 阶段一：产品策略占比汇总 ================")
    print(f"项目目录：{config.project_dir}")
    print(f"产品清单：{config.source_dir_name}\\{config.product_list_name}")
    print(f"策略分类表：{config.source_dir_name}\\{config.strategy_map_name}")
    print(f"估值表目录：{config.source_dir_name}\\{config.valuation_dir_name}")
    print(f"输出文件：{config.output_name}")
    print("日期核验：关闭")
    print("=========================================================\n")


def print_success_summary(stats: Stats, config: Config) -> None:
    print("\n================ 阶段一运行完成 ================")
    print(f"产品清单数量：{stats.product_count}")
    print(f"成功匹配估值表产品数量：{stats.valuation_matched_products}")
    print(f"未找到估值表产品数量：{stats.valuation_missing_products}")
    print(f"存在多个候选估值表产品数量：{stats.valuation_ambiguous_products}")
    print(f"估值表读取失败产品数量：{stats.valuation_read_failed_products}")
    print()
    print(f"扫描估值表行数：{stats.valuation_rows_scanned}")
    print(f"市价为空跳过行数：{stats.price_blank_rows}")
    print(f"科目代码不足6位跳过行数：{stats.short_code_rows}")
    print(f"子基金代码匹配成功：{stats.code_match_success}")
    print(f"子基金代码未匹配：{stats.code_match_failed}")
    print(f"子基金代码分类冲突：{stats.code_conflict_rows}")
    print(f"净值占比转换失败：{stats.ratio_parse_failed}")
    print()
    print(f"提取有效科目数量：{stats.valid_detail_rows}")
    print(f"生成策略汇总数量：{stats.strategy_summary_rows}")
    print(f"生成股票多头数量：{stats.stock_long_rows}")
    print()
    print(f"输出文件：{config.output_name}")
    print("输出工作表：科目比例明细")
    print("输出工作表：产品策略分类")
    print("===============================================")


def print_failure_summary(exc: PipelineFatalError) -> None:
    print(f"\n{Fore.RED}================ 阶段一运行失败 ================")
    print(f"失败阶段：{exc.stage}")
    print(f"失败文件：{exc.file}")
    print(f"失败原因：{exc.reason}")
    print(f"================================================{Style.RESET_ALL}")


def run_pipeline(config: Config = CONFIG) -> Stats:
    logger = Logger()
    stats = Stats()
    print_startup(config)

    valuation_files = ensure_inputs(config, logger)
    products = read_product_list(config, logger)
    stats.product_count = len(products)
    strategy_mapping = read_strategy_mapping(config, logger)
    valuation_index = build_valuation_index(valuation_files, config)

    all_detail_rows: list[dict[str, Any]] = []

    for product in products:
        logger.log(
            "产品读取",
            product=product,
            file=config.product_list_name,
            status="开始处理",
            level=LogLevel.DEFAULT,
        )

        match = match_valuation_file(
            product,
            valuation_files,
            valuation_index,
            config,
        )

        if match.status == "missing":
            stats.valuation_missing_products += 1
            logger.log(
                "估值表匹配",
                product=product,
                file="N/A",
                status="未找到对应估值表",
                level=LogLevel.ERROR,
            )
            continue

        if match.status == "ambiguous":
            stats.valuation_ambiguous_products += 1
            logger.log(
                "估值表匹配",
                product=product,
                file="N/A",
                status="找到多个候选估值表，需人工确认",
                level=LogLevel.WARNING,
            )
            for candidate in match.candidates:
                logger.candidate(candidate.name)
            continue

        assert match.selected is not None
        stats.valuation_matched_products += 1
        logger.log(
            "估值表匹配",
            product=product,
            file=match.selected.name,
            status="估值表匹配成功",
            level=LogLevel.SUCCESS,
        )

        product_rows = process_valuation_file(
            product=product,
            path=match.selected,
            mapping=strategy_mapping,
            config=config,
            logger=logger,
            stats=stats,
        )
        all_detail_rows.extend(product_rows)

    if not all_detail_rows:
        logger.log(
            "结果检查",
            file=config.output_name,
            status=(
                "没有提取到任何有效科目；请重点查看Terminal中的“估值表匹配”、"
                "“市价为空”和“代码后6位未找到策略分类”统计"
            ),
            level=LogLevel.ERROR,
        )

    detail, summary = build_outputs(
        all_detail_rows,
        products,
        config,
        logger,
        stats,
    )
    write_output(detail, summary, config, logger)
    print_success_summary(stats, config)
    return stats


def main() -> int:
    try:
        run_pipeline(CONFIG)
        return 0
    except PipelineFatalError as exc:
        print_failure_summary(exc)
        return 1
    except KeyboardInterrupt:
        exc = PipelineFatalError("用户中断", "N/A", "程序被手动终止")
        print_failure_summary(exc)
        return 130
    except Exception as exc:  # 最后的安全兜底，避免无说明退出。
        fatal = PipelineFatalError("未知阶段", "N/A", str(exc))
        print_failure_summary(fatal)
        return 1


if __name__ == "__main__":
    sys.exit(main())
