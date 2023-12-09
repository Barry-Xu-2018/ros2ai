# Copyright 2023 Tomoya Fujita <tomoya.fujita825@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ros2ai.api.config import OpenAiConfig

from openai import OpenAI


class ChatCompletionClient(OpenAiConfig):
    """
    Create single chat completion client w/o session and call OpenAI.
    """
    def __init__(self, args):
        # get OpenAI configuration
        super().__init__(args)

        self.client_ = OpenAI(
            api_key=self.get_value('api_key')
        )
        self.completion_ = None
        self.stream_ = True

    def call(self, sentence, stream=True):
        self.stream_ = stream
        try:
            self.completion_ = self.client_.chat.completions.create(
                model=self.get_value('api_model'),
                messages=[
                    {
                        "role": "user",
                        "content": f"{sentence}",
                    },
                ],
                stream=self.stream_,
                max_tokens=self.get_value('api_token')

            )
        except Exception as e:
            print('Failed to call OpenAI API: ' + str(e))
        else:
            pass

    def print_result(self):
        if self.completion_ is None:
            pass
        if self.stream_ is True:
            # TODO@fujitatomoya: check `finish_reason` in stream if available?
            for chunk in self.completion_:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
            print("\n")
        else:
            if (self.completion_.choices[0].finish_reason != 'stop'):
                print('Failed chat completion with: ' + self.completion_.choices[0].finish_reason)
            else:
                print(self.completion_.choices[0].message.content)

    def print_all(self):
        if self.stream_ is False:
            print(self.completion_)
