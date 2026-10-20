from pathlib import Path
from itertools import combinations
import re

import numpy as np
import pandas as pd
from scipy import stats


# ============================================================
# 1. 配置
# ============================================================

INPUT_PATH = Path(
    "/Users/qihang/Desktop/Qihang Studio/Careers/万家/滚动T检验"
)

OUTPUT_PATH = INPUT_PATH / "同向交易T检验结果.xlsx"

ALPHA = 0.05

# 至少2个R样本即可进行t检验
MIN_SAMPLE_N = 2

ZERO_EPS = 1e-12

WINDOWS = [1, 3, 5]


# ============================================================
# 2. 源数据字段
# ============================================================

COL_PRODUCT_CODE = "产品代码"
COL_PRODUCT_NAME = "产品名称"

COL_SECURITY_CODE = "基金代码"
COL_SECURITY_NAME = "基金名称"

COL_DIRECTION = "交易方向"

COL_PRICE = "成交价格"
COL_QTY = "成交数量"

COL_DATE = "成交日期"
COL_TIME = "成交时间"

COL_AMOUNT = "成交金额"


REQUIRED_COLUMNS = [
    COL_PRODUCT_CODE,
    COL_PRODUCT_NAME,
    COL_SECURITY_CODE,
    COL_SECURITY_NAME,
    COL_DIRECTION,
    COL_PRICE,
    COL_QTY,
    COL_DATE,
]


ILLEGAL_XML_RE = re.compile(
    r"[\x00-\x08\x0B\x0C\x0E-\x1F]"
)


# ============================================================
# 3. 基础清洗
# ============================================================

def clean_columns(df):

    df.columns = [
        str(c)
        .strip()
        .replace("\n", "")
        .replace("\r", "")
        for c in df.columns
    ]

    return df


def clean_code(value):

    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.endswith(".0"):
        text = text[:-2]

    return text


def clean_text(value):

    if pd.isna(value):
        return ""

    text = str(value).strip()

    return ILLEGAL_XML_RE.sub(
        "",
        text
    )


def normalize_direction(value):

    if pd.isna(value):
        return ""

    text = str(value).strip()

    if "买" in text:
        return "买入"

    if "卖" in text:
        return "卖出"

    return text


def parse_date_series(series):

    def parse_one(value):

        if pd.isna(value):
            return pd.NaT

        text = str(value).strip()

        if text.endswith(".0"):
            text = text[:-2]

        # YYYYMMDD
        if (
            len(text) == 8
            and text.isdigit()
        ):

            try:

                return pd.to_datetime(
                    text,
                    format="%Y%m%d"
                )

            except (
                ValueError,
                TypeError
            ):

                return pd.NaT

        # Excel serial date
        try:

            number = float(text)

            if 20000 <= number <= 80000:

                return pd.to_datetime(
                    number,
                    unit="D",
                    origin="1899-12-30"
                )

        except (
            ValueError,
            TypeError
        ):

            pass

        return pd.to_datetime(
            text,
            errors="coerce"
        )

    return series.apply(
        parse_one
    )


# ============================================================
# 4. 读取单个文件
# ============================================================

def read_source_file(path):

    frames = []

    suffix = path.suffix.lower()

    # ========================================================
    # Excel
    # ========================================================

    if suffix in [
        ".xlsx",
        ".xls"
    ]:

        try:

            excel = pd.ExcelFile(
                path
            )

        except Exception as e:

            print(
                f"[读取失败] {path.name}"
            )

            print(
                f"原因：{e}"
            )

            return frames

        for sheet_name in excel.sheet_names:

            try:

                df = pd.read_excel(
                    path,
                    sheet_name=sheet_name
                )

                df = clean_columns(
                    df
                )

                missing = [
                    col
                    for col in REQUIRED_COLUMNS
                    if col not in df.columns
                ]

                if missing:
                    continue

                df["_来源文件"] = path.name
                df["_来源Sheet"] = sheet_name

                frames.append(
                    df
                )

                print(
                    f"  [有效Sheet] "
                    f"{path.name} | "
                    f"{sheet_name}"
                )

            except Exception as e:

                print(
                    f"  [Sheet跳过] "
                    f"{path.name} | "
                    f"{sheet_name} | "
                    f"{e}"
                )

    # ========================================================
    # CSV
    # ========================================================

    elif suffix == ".csv":

        try:

            df = pd.read_csv(
                path
            )

            df = clean_columns(
                df
            )

            missing = [
                col
                for col in REQUIRED_COLUMNS
                if col not in df.columns
            ]

            if not missing:

                df["_来源文件"] = path.name
                df["_来源Sheet"] = ""

                frames.append(
                    df
                )

        except Exception as e:

            print(
                f"[CSV读取失败] "
                f"{path.name} | "
                f"{e}"
            )

    return frames


# ============================================================
# 5. 读取源数据
# ============================================================

def load_source_data():

    if not INPUT_PATH.exists():

        raise FileNotFoundError(
            f"找不到文件夹：\n"
            f"{INPUT_PATH}"
        )

    files = []

    for pattern in [
        "*.xlsx",
        "*.xls",
        "*.csv"
    ]:

        files.extend(
            INPUT_PATH.glob(
                pattern
            )
        )

    files = sorted(
        files,
        key=lambda x: x.name.lower()
    )

    frames = []

    for file in files:

        # Excel临时文件
        if file.name.startswith("~$"):
            continue

        # 本程序临时文件
        if file.name.startswith("~tmp_"):
            continue

        # 不读取自己的输出
        if (
            file.resolve()
            ==
            OUTPUT_PATH.resolve()
        ):
            continue

        print(
            f"\n读取：{file.name}"
        )

        frames.extend(
            read_source_file(
                file
            )
        )

    if not frames:

        raise ValueError(
            "没有找到包含所需字段的有效数据。"
        )

    return pd.concat(
        frames,
        ignore_index=True
    )


# ============================================================
# 6. 清洗交易数据
# ============================================================

def clean_trade_data(df):

    df = df.copy()

    # ========================================================
    # 代码
    # ========================================================

    df[COL_PRODUCT_CODE] = (
        df[COL_PRODUCT_CODE]
        .apply(clean_code)
    )

    df[COL_SECURITY_CODE] = (
        df[COL_SECURITY_CODE]
        .apply(clean_code)
    )

    # ========================================================
    # 名称
    # ========================================================

    df[COL_PRODUCT_NAME] = (
        df[COL_PRODUCT_NAME]
        .apply(clean_text)
    )

    df[COL_SECURITY_NAME] = (
        df[COL_SECURITY_NAME]
        .apply(clean_text)
    )

    # ========================================================
    # 买卖方向
    # ========================================================

    df[COL_DIRECTION] = (
        df[COL_DIRECTION]
        .apply(
            normalize_direction
        )
    )

    df = df[
        df[COL_DIRECTION].isin(
            [
                "买入",
                "卖出"
            ]
        )
    ].copy()

    # ========================================================
    # 数值
    # ========================================================

    df[COL_PRICE] = pd.to_numeric(
        df[COL_PRICE],
        errors="coerce"
    )

    df[COL_QTY] = pd.to_numeric(
        df[COL_QTY],
        errors="coerce"
    )

    # ========================================================
    # 日期
    # ========================================================

    df[COL_DATE] = parse_date_series(
        df[COL_DATE]
    )

    # ========================================================
    # 删除无效数据
    # ========================================================

    df = df.dropna(
        subset=[
            COL_PRICE,
            COL_QTY,
            COL_DATE
        ]
    )

    df = df[
        (df[COL_PRODUCT_CODE] != "")
        &
        (df[COL_SECURITY_CODE] != "")
        &
        (df[COL_PRICE] > 0)
        &
        (df[COL_QTY] > 0)
    ].copy()

    # 统一为00:00:00
    df["_交易日"] = (
        df[COL_DATE]
        .dt.normalize()
    )

    # VWAP分子
    df["_价量"] = (
        df[COL_PRICE]
        *
        df[COL_QTY]
    )

    return df


# ============================================================
# 7. 构建滚动窗口 VWAP
# ============================================================

def build_window_vwap(
    df,
    window_days
):
    """
    以每个实际交易日为中心。

    1日：
        d

    3日：
        d-1 ~ d+1

    5日：
        d-2 ~ d+2

    窗口内对：

    产品
    + 基金代码
    + 交易方向

    汇总VWAP。
    """

    radius = (
        window_days - 1
    ) // 2

    center_dates = sorted(
        df["_交易日"]
        .dropna()
        .unique()
    )

    all_windows = []

    for center_date in center_dates:

        center_date = pd.Timestamp(
            center_date
        )

        start_date = (
            center_date
            - pd.Timedelta(
                days=radius
            )
        )

        end_date = (
            center_date
            + pd.Timedelta(
                days=radius
            )
        )

        window_df = df[
            (
                df["_交易日"]
                >= start_date
            )
            &
            (
                df["_交易日"]
                <= end_date
            )
        ].copy()

        if window_df.empty:
            continue

        group_cols = [
            COL_PRODUCT_CODE,
            COL_SECURITY_CODE,
            COL_DIRECTION
        ]

        grouped = (
            window_df
            .groupby(
                group_cols,
                dropna=False
            )
            .agg(

                产品名称=(
                    COL_PRODUCT_NAME,
                    "first"
                ),

                基金名称=(
                    COL_SECURITY_NAME,
                    "first"
                ),

                成交数量=(
                    COL_QTY,
                    "sum"
                ),

                价量合计=(
                    "_价量",
                    "sum"
                ),

                原始成交笔数=(
                    COL_QTY,
                    "size"
                )
            )
            .reset_index()
        )

        grouped["VWAP"] = (
            grouped["价量合计"]
            /
            grouped["成交数量"]
        )

        grouped["中心日期"] = (
            center_date
        )

        grouped["窗口开始"] = (
            start_date
        )

        grouped["窗口结束"] = (
            end_date
        )

        grouped["窗口天数"] = (
            window_days
        )

        all_windows.append(
            grouped
        )

    if not all_windows:

        return pd.DataFrame()

    result = pd.concat(
        all_windows,
        ignore_index=True
    )

    return result


# ============================================================
# 8. 两两配对 + R_A / R_B
# ============================================================

def calculate_r_samples(
    vwap_df
):

    if vwap_df.empty:
        return pd.DataFrame()

    samples = []

    compare_cols = [
        "中心日期",
        COL_SECURITY_CODE,
        COL_DIRECTION
    ]

    for key, group in vwap_df.groupby(
        compare_cols,
        dropna=False
    ):

        if (
            group[
                COL_PRODUCT_CODE
            ].nunique()
            < 2
        ):
            continue

        group = group.sort_values(
            COL_PRODUCT_CODE
        )

        rows = group.to_dict(
            "records"
        )

        for a, b in combinations(
            rows,
            2
        ):

            if (
                a[COL_PRODUCT_CODE]
                ==
                b[COL_PRODUCT_CODE]
            ):
                continue

            p_a = float(
                a["VWAP"]
            )

            p_b = float(
                b["VWAP"]
            )

            q_a = float(
                a["成交数量"]
            )

            q_b = float(
                b["成交数量"]
            )

            matched_qty = min(
                q_a,
                q_b
            )

            direction = key[2]

            # =================================================
            # 买入
            # =================================================

            if direction == "买入":

                r_a = (
                    (p_b - p_a)
                    /
                    p_a
                    *
                    matched_qty
                    /
                    q_a
                )

                r_b = (
                    (p_a - p_b)
                    /
                    p_b
                    *
                    matched_qty
                    /
                    q_b
                )

            # =================================================
            # 卖出
            # =================================================

            else:

                r_a = (
                    (p_a - p_b)
                    /
                    p_a
                    *
                    matched_qty
                    /
                    q_a
                )

                r_b = (
                    (p_b - p_a)
                    /
                    p_b
                    *
                    matched_qty
                    /
                    q_b
                )

            samples.append({

                "中心日期":
                    key[0],

                "窗口开始":
                    a["窗口开始"],

                "窗口结束":
                    a["窗口结束"],

                "窗口天数":
                    a["窗口天数"],

                "基金代码":
                    key[1],

                "基金名称":
                    a["基金名称"],

                "委托方向":
                    direction,

                # A
                "组合A代码":
                    a[COL_PRODUCT_CODE],

                "组合A名称":
                    a["产品名称"],

                "VWAP_A":
                    p_a,

                "成交量_A":
                    q_a,

                "R_A":
                    r_a,

                # B
                "组合B代码":
                    b[COL_PRODUCT_CODE],

                "组合B名称":
                    b["产品名称"],

                "VWAP_B":
                    p_b,

                "成交量_B":
                    q_b,

                "R_B":
                    r_b,

                "共同成交量":
                    matched_qty,

                "A原始成交笔数":
                    a["原始成交笔数"],

                "B原始成交笔数":
                    b["原始成交笔数"]
            })

    return pd.DataFrame(
        samples
    )


# ============================================================
# 9. One-Sample t-Test
# ============================================================

def one_sample_t_test(
    values
):

    values = (
        pd.Series(values)
        .dropna()
        .astype(float)
    )

    n = len(values)

    if n == 0:
        return None

    mean = float(
        values.mean()
    )

    count_zero = int(
        (
            values.abs()
            <= ZERO_EPS
        ).sum()
    )

    count_positive = int(
        (
            values
            > ZERO_EPS
        ).sum()
    )

    count_negative = int(
        (
            values
            < -ZERO_EPS
        ).sum()
    )

    # ========================================================
    # 样本不足
    # ========================================================

    if n < MIN_SAMPLE_N:

        return {
            "n": n,
            "mean": mean,
            "std": np.nan,
            "t_stat": np.nan,
            "t_critical": np.nan,
            "df": n - 1,
            "p_value": np.nan,
            "pass": None,
            "zero": count_zero,
            "positive": count_positive,
            "negative": count_negative
        }

    std = float(
        values.std(
            ddof=1
        )
    )

    df = n - 1

    t_critical = float(
        stats.t.ppf(
            1 - ALPHA / 2,
            df
        )
    )

    # ========================================================
    # 标准差为0
    # ========================================================

    if abs(std) <= ZERO_EPS:

        if abs(mean) <= ZERO_EPS:

            t_stat = 0.0
            p_value = 1.0
            passed = True

        else:

            t_stat = np.nan
            p_value = 0.0
            passed = False

    # ========================================================
    # 正常 t-test
    # ========================================================

    else:

        result = stats.ttest_1samp(
            values,
            popmean=0,
            alternative="two-sided"
        )

        t_stat = float(
            result.statistic
        )

        p_value = float(
            result.pvalue
        )

        passed = (
            p_value >= ALPHA
        )

    return {
        "n": n,
        "mean": mean,
        "std": std,
        "t_stat": t_stat,
        "t_critical": t_critical,
        "df": df,
        "p_value": p_value,
        "pass": passed,
        "zero": count_zero,
        "positive": count_positive,
        "negative": count_negative
    }


# ============================================================
# 10. 汇总双向T检验
# ============================================================

def build_summary(samples):

    if samples.empty:
        return pd.DataFrame()

    output_rows = []

    # ========================================================
    # 一只基金 + 一组产品对 + 一个交易方向
    # 单独进行 t 检验
    # ========================================================

    group_cols = [
        "基金代码",
        "基金名称",

        "组合A代码",
        "组合A名称",

        "组合B代码",
        "组合B名称",

        "委托方向"
    ]

    for key, group in samples.groupby(
        group_cols,
        dropna=False
    ):

        (
            fund_code,
            fund_name,

            a_code,
            a_name,

            b_code,
            b_name,

            direction
        ) = key

        # ====================================================
        # A -> B
        # ====================================================

        result_a = one_sample_t_test(
            group["R_A"]
        )

        # ====================================================
        # B -> A
        # ====================================================

        result_b = one_sample_t_test(
            group["R_B"]
        )

        # ====================================================
        # 双向联合判定
        # ====================================================

        if (
            result_a["pass"] is None
            or
            result_b["pass"] is None
        ):

            pair_status = "样本不足"

        elif (
            result_a["pass"]
            and
            result_b["pass"]
        ):

            pair_status = "通过"

        else:

            pair_status = "未通过"

        # ====================================================
        # A -> B
        # ====================================================

        output_rows.append({

            "基金名称":
                fund_name,

            "基金代码":
                fund_code,

            "组合名称":
                a_name,

            "组合代码":
                a_code,

            "对比组合代码":
                b_code,

            "对比组合名称":
                b_name,

            "委托方向":
                direction,

            "溢价率均值":
                result_a["mean"],

            "溢价率标准差":
                result_a["std"],

            "T临界值":
                result_a["t_critical"],

            "自由度":
                result_a["df"],

            "p值":
                result_a["p_value"],

            "是否通过":
                pair_status,

            "=0?":
                result_a["zero"],

            ">0":
                result_a["positive"],

            "<0":
                result_a["negative"]
        })

        # ====================================================
        # B -> A
        # ====================================================

        output_rows.append({

            "基金名称":
                fund_name,

            "基金代码":
                fund_code,

            "组合名称":
                b_name,

            "组合代码":
                b_code,

            "对比组合代码":
                a_code,

            "对比组合名称":
                a_name,

            "委托方向":
                direction,

            "溢价率均值":
                result_b["mean"],

            "溢价率标准差":
                result_b["std"],

            "T临界值":
                result_b["t_critical"],

            "自由度":
                result_b["df"],

            "p值":
                result_b["p_value"],

            "是否通过":
                pair_status,

            "=0?":
                result_b["zero"],

            ">0":
                result_b["positive"],

            "<0":
                result_b["negative"]
        })

    return pd.DataFrame(
        output_rows
    )


# ============================================================
# 11. Excel安全清洗
# ============================================================

def sanitize_for_excel(
    df
):

    df = df.copy()

    df = df.replace(
        [
            np.inf,
            -np.inf
        ],
        np.nan
    )

    for column in df.columns:

        if (
            df[column].dtype
            == "object"
        ):

            df[column] = (
                df[column]
                .map(
                    lambda x:
                    ILLEGAL_XML_RE.sub(
                        "",
                        x
                    )
                    if isinstance(
                        x,
                        str
                    )
                    else x
                )
            )

    return df


# ============================================================
# 12. Excel格式
# ============================================================

def format_dataframe_sheet(
    writer,
    sheet_name,
    df,
    status_color=False
):

    worksheet = writer.sheets[
        sheet_name
    ]

    workbook = writer.book

    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#F2F2F2",
        "border": 1,
        "align": "center",
        "valign": "vcenter"
    })

    decimal_format = workbook.add_format({
        "num_format": "0.0000"
    })

    integer_format = workbook.add_format({
        "num_format": "0"
    })

    date_format = workbook.add_format({
        "num_format": "yyyy/mm/dd"
    })

    green_format = workbook.add_format({
        "bg_color": "#C6EFCE",
        "font_color": "#006100",
        "bold": True,
        "align": "center"
    })

    red_format = workbook.add_format({
        "bg_color": "#FFC7CE",
        "font_color": "#9C0006",
        "bold": True,
        "align": "center"
    })

    yellow_format = workbook.add_format({
        "bg_color": "#FFEB9C",
        "font_color": "#9C6500",
        "bold": True,
        "align": "center"
    })

    decimal_columns = {
        "溢价率均值",
        "溢价率标准差",
        "T临界值",
        "p值",
        "VWAP_A",
        "VWAP_B",
        "成交量_A",
        "成交量_B",
        "共同成交量",
        "R_A",
        "R_B"
    }

    integer_columns = {
        "自由度",
        "=0?",
        ">0",
        "<0",
        "窗口天数",
        "A原始成交笔数",
        "B原始成交笔数"
    }

    date_columns = {
        "中心日期",
        "窗口开始",
        "窗口结束"
    }

    rows, cols = df.shape

    worksheet.freeze_panes(
        1,
        0
    )

    if (
        rows > 0
        and cols > 0
    ):

        worksheet.autofilter(
            0,
            0,
            rows,
            cols - 1
        )

    # ========================================================
    # 表头
    # ========================================================

    for col_num, column_name in enumerate(
        df.columns
    ):

        worksheet.write(
            0,
            col_num,
            column_name,
            header_format
        )

    # ========================================================
    # 列宽及数字格式
    # ========================================================

    for col_num, column_name in enumerate(
        df.columns
    ):

        width = max(
            10,
            len(
                str(column_name)
            ) + 2
        )

        if rows > 0:

            values = (
                df[column_name]
                .head(500)
                .dropna()
                .astype(str)
            )

            if not values.empty:

                width = max(
                    width,
                    int(
                        values
                        .map(len)
                        .max()
                    ) + 2
                )

        width = min(
            width,
            30
        )

        if (
            column_name
            in decimal_columns
        ):

            worksheet.set_column(
                col_num,
                col_num,
                width,
                decimal_format
            )

        elif (
            column_name
            in integer_columns
        ):

            worksheet.set_column(
                col_num,
                col_num,
                width,
                integer_format
            )

        elif (
            column_name
            in date_columns
        ):

            worksheet.set_column(
                col_num,
                col_num,
                width,
                date_format
            )

        else:

            worksheet.set_column(
                col_num,
                col_num,
                width
            )

    # ========================================================
    # 状态着色
    # ========================================================

    if (
        status_color
        and
        "是否通过"
        in df.columns
    ):

        status_col = (
            df.columns
            .get_loc(
                "是否通过"
            )
        )

        for row_num, status in enumerate(
            df["是否通过"],
            start=1
        ):

            status = str(
                status
            ).strip()

            if status == "通过":

                fmt = green_format

            elif status == "未通过":

                fmt = red_format

            else:

                fmt = yellow_format

            worksheet.write(
                row_num,
                status_col,
                status,
                fmt
            )


# ============================================================
# 13. 输出Workbook
# ============================================================

def write_excel_output(
    all_results
):

    temp_output = (
        OUTPUT_PATH.with_name(
            "~tmp_同向交易T检验结果.xlsx"
        )
    )

    if temp_output.exists():

        try:
            temp_output.unlink()

        except OSError:
            pass

    with pd.ExcelWriter(
        temp_output,
        engine="xlsxwriter",
        datetime_format="yyyy/mm/dd",
        date_format="yyyy/mm/dd",
        engine_kwargs={
            "options": {
                "strings_to_urls": False,

                # 防止 =0? 被识别成公式
                "strings_to_formulas": False
            }
        }
    ) as writer:

        for window_days in WINDOWS:

            summary = sanitize_for_excel(
                all_results[
                    window_days
                ]["summary"]
            )

            samples = sanitize_for_excel(
                all_results[
                    window_days
                ]["samples"]
            )

            summary_sheet = (
                f"{window_days}日T检验"
            )

            detail_sheet = (
                f"{window_days}日R明细"
            )

            # =================================================
            # 汇总
            # =================================================

            summary.to_excel(
                writer,
                sheet_name=summary_sheet,
                index=False
            )

            format_dataframe_sheet(
                writer,
                summary_sheet,
                summary,
                status_color=True
            )

            # =================================================
            # R明细
            # =================================================

            samples.to_excel(
                writer,
                sheet_name=detail_sheet,
                index=False
            )

            format_dataframe_sheet(
                writer,
                detail_sheet,
                samples,
                status_color=False
            )

    temp_output.replace(
        OUTPUT_PATH
    )


# ============================================================
# 14. Main
# ============================================================

def main():

    print()
    print("=" * 60)
    print("万家基金 - 同向交易滚动 T 检验")
    print("窗口：1日 / 3日 / 5日")
    print("=" * 60)

    # ========================================================
    # Step 1
    # ========================================================

    print(
        "\n[1/3] 读取并清洗源数据"
    )

    source = load_source_data()

    print(
        f"原始记录数："
        f"{len(source):,}"
    )

    source = clean_trade_data(
        source
    )

    print(
        f"有效交易记录数："
        f"{len(source):,}"
    )

    # ========================================================
    # Step 2
    # ========================================================

    all_results = {}

    for window_days in WINDOWS:

        print()
        print(
            "=" * 60
        )

        print(
            f"[2/3] 计算 "
            f"{window_days} 日滚动窗口"
        )

        print(
            "=" * 60
        )

        # ----------------------------------------------------
        # VWAP
        # ----------------------------------------------------

        vwap_df = build_window_vwap(
            source,
            window_days
        )

        print(
            f"{window_days}日 VWAP记录："
            f"{len(vwap_df):,}"
        )

        # ----------------------------------------------------
        # R
        # ----------------------------------------------------

        samples = calculate_r_samples(
            vwap_df
        )

        print(
            f"{window_days}日 R样本："
            f"{len(samples):,}"
        )

        # ----------------------------------------------------
        # T-Test
        # ----------------------------------------------------

        summary = build_summary(
            samples
        )

        print(
            f"{window_days}日 T检验结果："
            f"{len(summary):,}"
        )

        all_results[
            window_days
        ] = {
            "summary":
                summary,

            "samples":
                samples
        }

    # ========================================================
    # Step 3
    # ========================================================

    print()
    print(
        "[3/3] 输出 Excel"
    )

    write_excel_output(
        all_results
    )

    print()
    print("=" * 60)
    print("处理完成")
    print("=" * 60)

    print(
        f"\n输出文件：\n"
        f"{OUTPUT_PATH}"
    )

    print()

    print(
        "Sheet："
    )

    for window_days in WINDOWS:

        print(
            f"  - {window_days}日T检验"
        )

        print(
            f"  - {window_days}日R明细"
        )

    print()


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    main()