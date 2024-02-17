def calc_scent_mds(gas_values):
  """_summary_

  Args:
      gas_values [[gas_value1,...gas_value10,diff_gas_value1,...dif_gas_value9] * 波の数]: gas_valueとdiff_gas_valueを含むリスト

  Returns:
      mds_result [[x{i},y{i}] * 波の数]: MDSで圧縮した結果
  """
  import numpy as np
  from sklearn.manifold import MDS

  mds = MDS(
    n_components=2, ## int,圧縮した後の次元の数
    metric=False, ## bool,比率尺度か否か
    n_init=4, ## int,SMACOFアルゴリズムを実行する初期化の回数
    max_iter=300, ## int,SMACOFアルゴリズムを実行する最大の回数
    verbose=0, ## int,詳細の表示
    eps=0.001, ## float,収束するための許容誤差
    n_jobs=None, ## int,並列処理の数
    random_state=None, ## int,乱数のシード
    dissimilarity='euclidean' ## {‘euclidean’, ‘precomputed’},ユークリッド距離を指定
  )

  np_gas_values = np.array(gas_values)

  transposed_gas_values = np_gas_values.T

  mds_result = mds.fit_transform(transposed_gas_values)

  return mds_result.tolist()