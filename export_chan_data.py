from Chan import CChan
from ChanConfig import CChanConfig
from Common.CEnum import AUTYPE, DATA_SRC, KL_TYPE, FX_TYPE
import pandas as pd
import argparse
from datetime import datetime


def export_fx_data(chan):
    """導出分型數據"""
    fx_data = []
    for kl_idx, kl_list in enumerate(chan.kl_datas.values()):
        lv = chan.lv_list[kl_idx]
        for klc in kl_list.lst:
            if klc.fx != FX_TYPE.UNKNOWN:
                fx_data.append({
                    'level': lv.name,
                    'time': klc.lst[0].time.to_str(),
                    'idx': klc.idx,
                    'fx_type': klc.fx.name,
                    'high': klc.high,
                    'low': klc.low
                })
    
    if fx_data:
        print("\n=== 分型數據 ===")
        df = pd.DataFrame(fx_data)
        print(df.to_string())
    else:
        print("\n沒有找到分型數據")


def export_bi_data(chan):
    """導出筆數據"""
    bi_data = []
    for kl_idx, kl_list in enumerate(chan.kl_datas.values()):
        lv = chan.lv_list[kl_idx]
        for bi in kl_list.bi_list:
            bi_data.append({
                'level': lv.name,
                'idx': bi.idx,
                'direction': bi.dir.name,
                'start_time': bi.begin_klc.lst[0].time.to_str(),
                'end_time': bi.end_klc.lst[0].time.to_str(),
                'start_val': bi.get_begin_val(),
                'end_val': bi.get_end_val(),
                'is_sure': bi.is_sure
            })
    
    if bi_data:
        print("\n=== 筆數據 ===")
        df = pd.DataFrame(bi_data)
        print(df.to_string())
    else:
        print("\n沒有找到筆數據")


def export_seg_data(chan):
    """導出線段數據"""
    seg_data = []
    for kl_idx, kl_list in enumerate(chan.kl_datas.values()):
        lv = chan.lv_list[kl_idx]
        for seg in kl_list.seg_list:
            seg_data.append({
                'level': lv.name,
                'idx': seg.idx,
                'direction': seg.dir.name,
                'start_time': seg.start_bi.begin_klc.lst[0].time.to_str(),
                'end_time': seg.end_bi.end_klc.lst[0].time.to_str(),
                'start_val': seg.start_bi.get_begin_val(),
                'end_val': seg.end_bi.get_end_val(),
                'is_sure': seg.is_sure
            })
    
    if seg_data:
        print("\n=== 線段數據 ===")
        df = pd.DataFrame(seg_data)
        print(df.to_string())
    else:
        print("\n沒有找到線段數據")


def export_zs_data(chan):
    """導出中樞數據"""
    zs_data = []
    for kl_idx, kl_list in enumerate(chan.kl_datas.values()):
        lv = chan.lv_list[kl_idx]
        for zs in kl_list.zs_list:
            zs_data.append({
                'level': lv.name,
                'type': '筆中樞',
                'start_time': zs.begin.time.to_str(),
                'end_time': zs.end.time.to_str(),
                'high': zs.high,
                'low': zs.low,
                'is_sure': zs.is_sure
            })
        
        for segzs in kl_list.segzs_list:
            zs_data.append({
                'level': lv.name,
                'type': '段中樞',
                'start_time': segzs.begin.time.to_str(),
                'end_time': segzs.end.time.to_str(),
                'high': segzs.high,
                'low': segzs.low,
                'is_sure': segzs.is_sure
            })
    
    if zs_data:
        print("\n=== 中樞數據 ===")
        df = pd.DataFrame(zs_data)
        print(df.to_string())
    else:
        print("\n沒有找到中樞數據")


def export_bs_point_data(chan):
    """導出買賣點數據"""
    bs_data = []
    for kl_idx, kl_list in enumerate(chan.kl_datas.values()):
        lv = chan.lv_list[kl_idx]
        
        # 筆買賣點
        for bs_point in kl_list.bs_point_lst.bsp_iter():
            bs_data.append({
                'level': lv.name,
                'type': '筆買賣點',
                'bs_type': bs_point.type2str(),
                'is_buy': bs_point.is_buy,
                'time': bs_point.klu.time.to_str(),
                'price': bs_point.klu.low if bs_point.is_buy else bs_point.klu.high
            })
        
        # 段買賣點
        for seg_bs_point in kl_list.seg_bs_point_lst.bsp_iter():
            bs_data.append({
                'level': lv.name,
                'type': '段買賣點',
                'bs_type': seg_bs_point.type2str(),
                'is_buy': seg_bs_point.is_buy,
                'time': seg_bs_point.klu.time.to_str(),
                'price': seg_bs_point.klu.low if seg_bs_point.is_buy else seg_bs_point.klu.high
            })
    
    if bs_data:
        print("\n=== 買賣點數據 ===")
        df = pd.DataFrame(bs_data)
        print(df.to_string())
    else:
        print("\n沒有找到買賣點數據")


def export_all_data(code, begin_time, end_time, data_src, lv_list):
    """導出所有缠論數據"""
    # 配置缠論參數
    config = CChanConfig({
        "bi_strict": True,
        "trigger_step": False,
        "skip_step": 0,
        "divergence_rate": float("inf"),
        "bsp2_follow_1": False,
        "bsp3_follow_1": False,
        "min_zs_cnt": 0,
        "bs1_peak": False,
        "macd_algo": "peak",
        "bs_type": '1,2,3a,1p,2s,3b',
        "print_warning": False,  # 關閉警告輸出，避免干擾數據顯示
        "zs_algo": "normal",
    })
    
    # 創建 CChan 實例
    print(f"正在加載數據，請稍候...")
    chan = CChan(
        code=code,
        begin_time=begin_time,
        end_time=end_time,
        data_src=data_src,
        lv_list=lv_list,
        config=config,
        autype=AUTYPE.QFQ,
    )
    
    # 打印基本信息
    print("\n=== 基本信息 ===")
    print(f"股票代碼: {code}")
    print(f"開始時間: {begin_time}")
    print(f"結束時間: {end_time if end_time else '至今'}")
    print(f"數據源: {data_src.name if hasattr(data_src, 'name') else data_src}")
    print(f"級別列表: {', '.join([lv.name for lv in lv_list])}")
    print(f"分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 導出各類數據
    export_fx_data(chan)
    export_bi_data(chan)
    export_seg_data(chan)
    export_zs_data(chan)
    export_bs_point_data(chan)
    
    print("\n=== 分析完成 ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='導出缠論技術分析數據')
    parser.add_argument('--code', type=str, required=True, help='股票代碼，例如：sh.601799')
    parser.add_argument('--begin_time', type=str, required=True, help='開始時間，例如：2024-01-01')
    parser.add_argument('--end_time', type=str, help='結束時間，例如：2024-10-01，不指定則為當前時間')
    parser.add_argument('--data_src', type=str, default='BAO_STOCK', 
                        choices=['BAO_STOCK', 'CCXT', 'CSV'], 
                        help='數據源')
    parser.add_argument('--levels', type=str, default='DAY', 
                        help='K線級別，用逗號分隔，例如：DAY,60M,30M,15M,5M')
    
    args = parser.parse_args()
    
    # 解析K線級別
    level_map = {
        'DAY': KL_TYPE.K_DAY,
        '60M': KL_TYPE.K_60M,
        '30M': KL_TYPE.K_30M,
        '15M': KL_TYPE.K_15M,
        '5M': KL_TYPE.K_5M,
        'WEEK': KL_TYPE.K_WEEK,
        'MON': KL_TYPE.K_MON
    }
    
    lv_list = [level_map[lv] for lv in args.levels.split(',') if lv in level_map]
    if not lv_list:
        lv_list = [KL_TYPE.K_DAY]
    
    # 解析數據源
    data_src_map = {
        'BAO_STOCK': DATA_SRC.BAO_STOCK,
        'CCXT': DATA_SRC.CCXT,
        'CSV': DATA_SRC.CSV
    }
    data_src = data_src_map.get(args.data_src, DATA_SRC.BAO_STOCK)
    
    # 導出數據
    try:
        export_all_data(args.code, args.begin_time, args.end_time, data_src, lv_list)
    except Exception as e:
        print(f"錯誤: {e}")
