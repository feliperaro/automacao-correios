"""Automação Correios"""

import json
import sys
import chromedriver
import gvars
from filelog import filelog as log

def consulta_encomenda(*, driver, objeto_rastreio: str):
    """Consulta encomenda nos Correios"""
    log("[INICIO] consulta_encomenda()")

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
    log(f"url: {url}")
    driver.get(url=url)

    output = {"status": None, "code": objeto_rastreio, "data": {}}
    for script in scripts:
        log(f"script: {script}")

        return_script = chromedriver.wait_execute_script(driver=driver, script=script["script"])
        log(f"return_script: {return_script}")

        if script["name"] == "error":
            is_error = return_script
            log(f"is_error: {is_error}")
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
            log(f"title: {title}")
            output["data"]["title"] = title
        elif script["name"] == "message":
            message = return_script
            log(f"message: {message}")
            output["data"]["message"] = message

    log(f"output: {json.dumps(output, ensure_ascii=False, indent=4)}")
    driver.close()

    file_path = gvars. path_output + "\\output.json"
    log(f"file_path: {file_path}")

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=2)

    log("[FIM] consulta_encomenda()")
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
        log("testing for...", case["test_case_name"])
        chrome = chromedriver.open_chrome()
        result = consulta_encomenda(driver=chrome, objeto_rastreio=case["objeto_rastreio"])
        log(f"result: {result}")
        expected_result = case["expected_result"]
        log(f"expected_result: {expected_result}")
        assert result == expected_result
        log("consulta_encomenda(): success!")


if __name__ == "__main__":
    try:
        if gvars.ENV == "dev":
            test_consulta_encomenda()
        else:
            args = sys.argv
            if len(args) != 2:
                log("Usage: python consulta_encomenda.py codigo_encomenda")
                sys.exit()

            codigo_encomenda = args[1]
            driver_chrome = chromedriver.open_chrome()
            consulta_encomenda(driver=driver_chrome, objeto_rastreio=codigo_encomenda)
    except KeyboardInterrupt:
        log("stopping by keyboard interrupt")
    except Exception as error:
        log(f"error: {error}")
        