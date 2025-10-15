import argparse
import numpy as np
from scipy import constants

# 物理定数の定義
C_LIGHT = constants.c          # 自由空間光速 u0 (m/s)
EPSILON_0 = constants.epsilon_0  # 自由空間の誘電率 E0 (F/m)

# -------------------------------------------------------------------
# 1. 理想的な理論長 L_theory の計算
# -------------------------------------------------------------------
def calculate_cpw_length_quarter_wave(frequency_ghz, ref_index, mode_k):
    """
    一端を短絡したクォーター波長CPW共振器の理想的な理論長を計算する (mm単位)。
    """
    frequency_hz = frequency_ghz * 1e9
    effective_epsilon = ref_index**2
    
    # L_theory (m) = (k * c) / (4 * f * sqrt(E_eff))
    length_m = (mode_k * C_LIGHT) / (4 * frequency_hz * np.sqrt(effective_epsilon))
    
    return length_m * 1000 # mmに変換

# -------------------------------------------------------------------
# 2. Getsingerの近似式 L_sc の計算 (ユーザー提供関数)
# -------------------------------------------------------------------
def calculate_Lsc_getsinger(S, W, Z0, E_eff, E0=EPSILON_0):
    """
    Getsingerの近似式に基づき、CPW短絡端インダクタンス L_sc を計算する (H単位)。
    S, W は [m] 単位で入力すること。
    """
    cosh_arg = (60 * np.pi**2) / (Z0 * np.sqrt(E_eff))
    correction_term = 2.0 - (1.0 / np.cosh(cosh_arg))
    
    # 係数部分: (2 / pi) * (S + W) * E0 * Z0 * sqrt(E_eff)
    coefficient = (2.0 / np.pi) * (S + W) * E0 * Z0 * np.sqrt(E_eff)
    
    L_sc = coefficient * correction_term
    
    return L_sc

# -------------------------------------------------------------------
# 3. 実効過剰長さ ell_sc の計算 (ユーザー提供関数)
# -------------------------------------------------------------------
def calculate_ell_sc(L_sc, Z0, E_eff, f):
    """
    L_sc (H)を、動作周波数 f (Hz)における実効過剰長さ ell_sc (m)に変換する。
    """
    omega = 2.0 * np.pi * f
    
    # 正規化リアクタンス x_sc = (omega * L_sc) / Z0
    X_sc = omega * L_sc
    x_sc = X_sc / Z0
    
    # 位相定数 beta = (omega * sqrt(E_eff)) / u_0
    beta = (omega * np.sqrt(E_eff)) / C_LIGHT
    
    # 実効過剰長さ ell_sc (m) = arctan(x_sc) / beta
    ell_sc = np.arctan(x_sc) / beta
    
    return ell_sc

# -------------------------------------------------------------------
# メイン実行ブロック
# -------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Getsingerの近似式に基づき、CPW短絡端補正を適用した共振器の長さを計算します。")
    parser.add_argument("frequency", type=float, help="目標とする共振周波数 (GHz)")
    parser.add_argument("--ref_index", type=float, default=2.5, help="CPWの実効屈折率 (デフォルト: 2.5)")
    parser.add_argument("--mode_k", type=int, default=1, help="共振モードの次数 (奇数のみ, デフォルト: 1)")
    
    # Getsingerの近似式に必要な新しい引数
    parser.add_argument("--center_width_um", type=float, required=True, help="中心導体の幅 S (マイクロメートル: um)")
    parser.add_argument("--slot_width_um", type=float, required=True, help="スロット幅 W (マイクロメートル: um)")
    parser.add_argument("--impedance", type=float, required=True, help="特性インピーダンス Z0 (オーム: Ω)")
    
    args = parser.parse_args()
    
    # --- 単位変換 ---
    f_hz = args.frequency * 1e9 # GHz -> Hz
    S_m = args.center_width_um * 1e-6 # um -> m
    W_m = args.slot_width_um * 1e-6 # um -> m
    Z0 = args.impedance # Ω
    E_eff = args.ref_index**2 # E_eff
    
    # --- 計算実行 ---
    
    # 1. 理想的な理論長 (補正なし) の計算
    theory_length_mm = calculate_cpw_length_quarter_wave(args.frequency, args.ref_index, args.mode_k)
    
    # 2. Getsingerの式による短絡端インダクタンス L_sc (H) の計算
    L_sc_h = calculate_Lsc_getsinger(S_m, W_m, Z0, E_eff)
    
    # 3. L_sc を実効過剰長さ ell_sc (m) に変換し、mm単位に
    ell_sc_m = calculate_ell_sc(L_sc_h, Z0, E_eff, f_hz)
    ell_sc_mm = ell_sc_m * 1000 # m -> mm
    
    # 4. 最終設計長 (L_final = L_theory - ell_sc)
    corrected_length_mm = theory_length_mm - ell_sc_mm
    
    # --- 結果の表示 ---
    print("--- CPWの長さ計算結果（Getsinger短絡端補正あり）---")
    print(f"目標周波数: {args.frequency:.2f} GHz")
    print(f"特性インピーダンス Z0: {Z0:.2f} Ω")
    print(f"実効誘電率 E_eff: {E_eff:.3f}")
    print("------------------------------------------")
    print(f"理論長 (補正なし): {theory_length_mm:.3f} mm")
    print(f"短絡端インダクタンス L_sc: {L_sc_h * 1e12:.3f} pH")
    print(f"Getsinger補正値 (ell_sc): -{ell_sc_mm:.3f} mm")
    print(f"必要なCPWの最終設計長さ: {corrected_length_mm:.3f} mm")
