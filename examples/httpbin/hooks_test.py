# NOTICE: Generated By HttpRunner. DO'NOT EDIT!
# FROM: examples/httpbin/hooks.yml
from httprunner import HttpRunner, TConfig, TStep


class TestCaseHooks(HttpRunner):
    config = TConfig(
        **{
            "name": "basic test with httpbin",
            "base_url": "${get_httpbin_server()}",
            "setup_hooks": ["${hook_print(setup)}"],
            "teardown_hooks": ["${hook_print(teardown)}"],
            "path": "examples/httpbin/hooks_test.py",
        }
    )

    teststeps = [
        TStep(
            **{
                "name": "headers",
                "variables": {"a": 123},
                "request": {"url": "/headers", "method": "GET"},
                "setup_hooks": [
                    "${setup_hook_add_kwargs($request)}",
                    "${setup_hook_remove_kwargs($request)}",
                ],
                "teardown_hooks": ["${teardown_hook_sleep_N_secs($response, 1)}"],
                "validate": [
                    {"eq": ["status_code", 200]},
                    {"contained_by": ["body.headers.Host", "${get_httpbin_server()}"]},
                ],
            }
        ),
        TStep(
            **{
                "name": "alter response",
                "request": {"url": "/headers", "method": "GET"},
                "teardown_hooks": ["${alter_response($response)}"],
                "validate": [
                    {"eq": ["status_code", 200]},
                    {"eq": ["body.headers.Host", "httpbin.org"]},
                ],
            }
        ),
    ]


if __name__ == "__main__":
    TestCaseHooks().test_start()
