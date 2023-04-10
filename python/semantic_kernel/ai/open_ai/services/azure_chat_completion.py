# Copyright (c) Microsoft. All rights reserved.


from logging import Logger
from typing import Any, Optional

from semantic_kernel.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)


class AzureChatCompletion(OpenAIChatCompletion):
    _endpoint: str
    _api_version: str
    _api_type: str

    def __init__(
        self,
        deployment_name: str,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = "2023-03-15-preview",
        logger: Optional[Logger] = None,
        ad_auth=False,
    ) -> None:
        """
        Initialize an AzureChatCompletion backend.

        You must provide:
        - A deployment_name, endpoint, and api_key (plus, optionally: ad_auth)

        :param deployment_name: The name of the Azure deployment. This value
            will correspond to the custom name you chose for your deployment
            when you deployed a model. This value can be found under
            Resource Management > Deployments in the Azure portal or, alternatively,
            under Management > Deployments in Azure OpenAI Studio.
        :param endpoint: The endpoint of the Azure deployment. This value
            can be found in the Keys & Endpoint section when examining
            your resource from the Azure portal.
        :param api_key: The API key for the Azure deployment. This value can be
            found in the Keys & Endpoint section when examining your resource in
            the Azure portal. You can use either KEY1 or KEY2.
        :param api_version: The API version to use. (Optional)
            The default value is "2022-12-01".
        :param logger: The logger instance to use. (Optional)
        :param ad_auth: Whether to use Azure Active Directory authentication.
            (Optional) The default value is False.
        """
        if endpoint is None and api_key is None:
            from synapse.ml.mlflow import get_mlflow_env_config

            mlflow_env_config = get_mlflow_env_config()
            api_key, endpoint = (
                mlflow_env_config.driver_aad_token,
                f"{mlflow_env_config.workload_endpoint}cognitive/openai",
            )
            ad_auth = True

        if not deployment_name:
            raise ValueError("The deployment name cannot be `None` or empty")
        if not api_key:
            raise ValueError("The Azure API key cannot be `None` or empty`")
        if not endpoint:
            raise ValueError("The Azure endpoint cannot be `None` or empty")
        if not endpoint.startswith("https://"):
            raise ValueError("The Azure endpoint must start with https://")

        self._endpoint = endpoint
        self._api_version = api_version
        self._api_type = "azure_ad" if ad_auth else "azure"

        super().__init__(deployment_name, api_key, org_id=None, log=logger)

    def _setup_open_ai(self) -> Any:
        import openai

        openai.api_type = self._api_type
        openai.api_key = self._api_key
        openai.api_base = self._endpoint
        openai.api_version = self._api_version

        return openai
