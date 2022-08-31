import argparse

import config
from textra import ApiClient

if __name__ == '__main__':
    def translate_ej(text: str) -> str:
        return ApiClient(**config.textra_api).generalNT_en_ja(text)

    def translate_je(text: str) -> str:
        return ApiClient(**config.textra_api).generalNT_ja_en(text)

    translator_dict = {
        'ej': translate_ej,
        'je': translate_je,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('translation_type', type=str, choices=translator_dict.keys(), help='translation type')
    parser.add_argument('text', type=str, help='source text')
    args = parser.parse_args()

    ret = translator_dict[args.translation_type](args.text)
    print(ret)
