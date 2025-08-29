from bambooai.template_formatting import CodeGenPromptGenerator


def test_format_section_xml_yaml():
    gen = CodeGenPromptGenerator({}, {})
    result = gen.format_section('key: value', 'xml', 'Plan')
    assert result.startswith('<plan>')
    assert '```yaml' in result
    assert 'key: value' in result


def test_select_template():
    gen = CodeGenPromptGenerator({}, {})
    assert gen.select_template('Data Analyst DF', True, 'm', []) == 'code_generator_user_df_plan'
    assert gen.select_template('Data Analyst DF', False, 'm', []) == 'code_generator_user_df_no_plan'
    assert gen.select_template('Other', True, 'm', []) == 'code_generator_user_gen_plan'
    assert gen.select_template('Other', False, 'm', []) == 'code_generator_user_gen_no_plan'


def test_generate_prompt_no_plan(tmp_path):
    templates = {
        'code_generator_user_df_no_plan': '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'
    }
    model_dict = {'gpt': {'templ_formating': 'text'}}
    gen = CodeGenPromptGenerator(templates, model_dict)
    prompt = gen.generate_prompt(
        generated_datasets_path=str(tmp_path),
        analyst='Data Analyst DF',
        planning=False,
        model='gpt',
        reasoning_models=[],
        plan_or_context='ctx',
        dataframe_head='dfh',
        auxiliary_datasets='aux',
        data_model='model',
        task='do something',
        python_version='3',
        pandas_version='1',
        plotly_version='2',
        previous_results='prev',
        example_code='example'
    )
    sections = [
        'CONTEXT:\n```yaml\nctx\n```',
        'DATAFRAME:\ndfh',
        'AUXILIARY DATASETS:\naux',
        f'GENERATED DATASETS PATH INSTRUCTION:\n{str(tmp_path)}/<descriptive_name>.csv',
        'DATA MODEL AND HELPER FUNCTIONS:\n```yaml\nmodel\n```',
        'TASK:\ndo something',
        'PYTHON VERSION:\n3',
        'PANDAS VERSION:\n1',
        'PLOTLY VERSION:\n2',
        'PREVIOUS RESULTS:\nprev',
        'EXAMPLE CODE:\nexample'
    ]
    expected = '|'.join(sections)
    assert prompt == expected
