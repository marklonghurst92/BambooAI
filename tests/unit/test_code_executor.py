import pandas as pd
from pandas.testing import assert_frame_equal

from bambooai.code_executor import CodeExecutor


def test_execute_local_success(tmp_path):
    df = pd.DataFrame({'a': [1, 2]})
    executor = CodeExecutor(mode='local')
    code = "df['b'] = df['a'] * 2\nprint('done')"
    result_df, results, error, plots, datasets = executor.execute(
        code, df, generated_datasets_path=str(tmp_path)
    )

    assert error is None
    assert 'done' in results
    assert result_df['b'].tolist() == [2, 4]
    assert plots == []
    assert datasets == []


def test_execute_local_error(tmp_path):
    df = pd.DataFrame({'a': [1, 2]})
    executor = CodeExecutor(mode='local')
    code = "df = df_nonexistent"
    result_df, results, error, plots, datasets = executor.execute(
        code, df, generated_datasets_path=str(tmp_path)
    )

    assert_frame_equal(result_df, df)
    assert results is None
    assert 'NameError' in error
    assert plots == []
    assert datasets == []
