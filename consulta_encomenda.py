"""Automação Correios"""

import json
import sys
import chromedriver
import gvars


def consulta_encomenda(*, driver, objeto_rastreio: str):
    """Consulta encomenda nos Correios"""

    scripts = [
        {
            "name": "error",
            "script": "document.getElementsByTagName('h1')[0].innerHTML === 'Opa!'"
        },
        {
            "name": "title",
            "script": "document.getElementsByClassName('my-14')[0].children[0].innerHTML"
        },
        {
            "name": "message",
            "script": "document.getElementsByClassName('my-14')[0].children[1].innerHTML"
        },
    ]

    url = gvars.URL_CORREIOS + objeto_rastreio
    driver.get(url=url)

    output = {"status": None, "code": objeto_rastreio, "data": {}}
    for script in scripts:
        return_script = chromedriver.wait_execute_script(driver=driver, script=script["script"])
        if script["name"] == "error":
            is_error = return_script
            if is_error:
                status = "error"
            else:
                status = "success"
            output["status"] = status
            if is_error:
                output["data"] = None
                break

        if script["name"] == "title":
            title = return_script
            output["data"]["title"] = title
        elif script["name"] == "message":
            message = return_script
            output["data"]["message"] = message

    driver.close()

    file_path = "output\\output.json"
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=2)

    if is_error:
        return -1

    return 1


def test_consulta_encomenda():
    """Testing function consulta_encomenda()"""

    tests_cases = [
        {
            "test_case_name": "error",
            "objeto_rastreio": "0000000000000",
            "expected_result": -1,
        },
        {
            "test_case_name": "success",
            "objeto_rastreio": "LB571181225HK",
            "expected_result": 1,
        },
    ]

    for case in tests_cases:
        print("testing for...", case["test_case_name"])
        chrome = chromedriver.open_chrome()
        result = consulta_encomenda(driver=chrome, objeto_rastreio=case["objeto_rastreio"])
        print("result: ", result)
        expected_result = case["expected_result"]
        print("expected_result: ", expected_result)
        assert result == expected_result
        print("consulta_encomenda(): success!")


if __name__ == "__main__":
    try:
        if gvars.ENV == "dev":
            test_consulta_encomenda()
        else:
            args = sys.argv
            if len(args) != 2:
                print("Usage: python consulta_encomenda.py codigo_encomenda")
                sys.exit()

            codigo_rastreio = args[1]
            driver_chrome = chromedriver.open_chrome()
            consulta_encomenda(driver=driver_chrome, objeto_rastreio=codigo_rastreio)
    except KeyboardInterrupt as error:
        print("error", error)
