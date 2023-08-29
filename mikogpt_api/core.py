from typing import List

import requests
import json


class MikogptAPI:
    """
    An object that allows you to make requests to the "mikogpt.ru" API by methods: `chat_completion`
    """

    def __init__(self, key, api_version=1):
        """
        Create new MikogptAPI Object

        :param key: private api key
        :param api_version: version of api (didn't require to change)
        """
        self._key = key
        self._api_version = api_version
        self._base_url = "http://api.mikogpt.ru"

    def _build_request_object(self, data):
        return {"key": self._key, "version": self._api_version, "data": data}

    def chat_completion(self, messages: list[[str, str]]):
        """
        Make chat completion request

        :param messages: A list of `[author, message]` objects pairs
        :return: MikogptAPIResponse object with response data
        :raise MikogptAPIResponse:
        """
        return MikogptAPIResponse.from_chat_completion(
            requests.post(
                self._base_url + "/chat",
                json=self._build_request_object(messages)
            )
        )


class MikogptAPIResponseException(Exception):
    """
    Raises when api response with exception
    """
    def __init__(self, error_code):
        self.error_code = error_code
        super().__init__(f"MikogptAPI response with exception: \"{error_code}\"")


class MikogptAPIResponse:
    def __init__(self, status: str):
        self.status = status
        self.error = None
        if self.status != "Success":
            self.error = self.status

    @staticmethod
    def from_chat_completion(response):
        txt = response.text
        response = json.loads(txt)
        output = MikogptAPIResponse(response["status"])
        if output.error:
            raise MikogptAPIResponseException(output.error)
        return output
