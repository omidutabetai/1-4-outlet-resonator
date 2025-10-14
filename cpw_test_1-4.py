import argparse
import numpy as np

def calculate_cpw_length_quarter_wave(frequency_ghz, ref_index, mode_k):
    """
    一端を短絡したクォーター波長CPW共振器の長さを計算します。

    Args:
        frequency_ghz (float): 共振周波数 (単位: GHz)。
        ref_index (float): CPWの屈折率。
        mode_k (int): 共振モードの次数 (奇数のみ: k=1, 3, 5...)。

    Returns:
        float: CPWの長さ (単位: mm)。
    """
    # 光速 (単位: m/s)
    c_light = 299792458
    
    # 周波数をHzに変換
    frequency_hz = frequency_ghz * 1e9
    
    # 屈折率から実効誘電率を計算
    effective_epsilon = ref_index**2
    
    # 長さを計算 (単位: m)
    # L = (k * c) / (4 * f * sqrt(effective_epsilon))
    length_m = (mode_k * c_light) / (4 * frequency_hz * np.sqrt(effective_epsilon))
    
    # 結果をmmに変換して返す
    return length_m * 1000

if __name__ == "__main__":
    # 引数パーサーの設定
    parser = argparse.ArgumentParser(description="一端を短絡したクォーター波長CPW共振器の長さを計算するスクリプトです。")
    parser.add_argument("frequency", type=float, help="目標とする共振周波数 (GHz)")
    parser.add_argument("--ref_index", type=float, default=2.5, help="CPWの屈折率 (デフォルト: 2.5)")
    parser.add_argument("--mode_k", type=int, default=1, help="共振モードの次数 (奇数のみ, デフォルト: 1)")
    
    # 引数のパース
    args = parser.parse_args()
    
    # 計算の実行
    cpw_length_mm = calculate_cpw_length_quarter_wave(args.frequency, args.ref_index, args.mode_k)
    
    # 結果の表示
    print("--- CPWの長さ計算結果 ---")
    print(f"周波数: {args.frequency} GHz")
    print(f"屈折率: {args.ref_index}")
    print(f"モード次数: {args.mode_k}")
    print(f"必要なCPWの長さ: {cpw_length_mm:.2f} mm")
