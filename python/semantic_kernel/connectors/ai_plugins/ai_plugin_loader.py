# Copyright (c) Microsoft. All rights reserved.

from requests import get
from yaml import safe_load


class AIPluginLoader:
    def __init__(self, plugin_url: str):
        self.plugin_url = plugin_url
        self.plugin_spec = None
        self.plugin_openapi_spec = None

    def load(self) -> None:
        from openapi3 import OpenAPI
        
        # First, load the plugin URL and look for
        # the /.well-known/a-plugin.json file
        self.plugin_spec = get(f"{self.plugin_url}/.well-known/a-plugin.json").json()

        # Validate the plugin spec
        if not self.plugin_spec:
            raise ValueError("Plugin spec not found")
        if "api" not in self.plugin_spec:
            raise ValueError("Plugin spec must contain an 'api' section")
        if "url" not in self.plugin_spec["api"]:
            raise ValueError("Plugin spec must contain an 'api.url' value")

        # Now extract the "api.url" and load the OpenAPI spec
        openai_yaml = get(self.plugin_spec["api"]["url"]).text

        # Next, load up the OpenAPI spec
        self.plugin_openapi_spec = OpenAPI(safe_load(openai_yaml))

    
    def to_native_function(self, path):
        # TODO: Think about how we do this...
        # parameters = []
        # for param in method.__sk_function_context_parameters__:
            
        #     parameters.append(
        #         ParameterView(
        #             param["name"], param["description"], param["default_value"]
        #         )
        #     )

        # if hasattr(method, "__sk_function_input_description__"):
        #     input_param = ParameterView(
        #         "input",
        #         method.__sk_function_input_description__,
        #         method.__sk_function_input_default_value__,
        #     )
        #     parameters = [input_param] + parameters

        # return SKFunction(
        #     delegate_type=DelegateInference.infer_delegate_type(method),
        #     delegate_function=method,
        #     parameters=parameters,
        #     description=method.__sk_function_description__,
        #     skill_name=skill_name,
        #     function_name=method.__sk_function_name__,
        #     is_semantic=False,
        #     log=log,
        # )



