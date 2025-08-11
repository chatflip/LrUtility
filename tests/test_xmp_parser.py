from pathlib import Path

import pytest

from xmp_parser import parse_xmp_file


class TestXmpParser:
    """XMPパーサーのテストクラス。"""

    def test_rating_xmp(self) -> None:
        """rating_1.xmpからRawImageNameとRatingを正しく取得できることを確認。"""
        xmp_file = Path("tests/assets/rating_1.xmp")
        metadata = parse_xmp_file(xmp_file)

        # RawImageNameの確認
        assert metadata.camera_raw_settings.raw_file_name == "rating_1.ARW"

        # Ratingの確認（1が設定されている）
        assert metadata.xmp_info.rating == 1

    def test_not_rating_xmp(self) -> None:
        """not_rating.xmpからRawImageNameを取得し、Ratingがないことを確認。"""
        xmp_file = Path("tests/assets/not_rating.xmp")
        metadata = parse_xmp_file(xmp_file)

        # RawImageNameの確認
        assert metadata.camera_raw_settings.raw_file_name == "not_rating.ARW"

        # Ratingの確認（設定されていないのでNone）
        assert metadata.xmp_info.rating is None

    def test_file_not_found(self) -> None:
        """存在しないファイルに対してFileNotFoundErrorが発生することを確認。"""
        non_existent_file = Path("tests/assets/non_existent.xmp")
        with pytest.raises(FileNotFoundError, match="XMP file not found"):
            parse_xmp_file(non_existent_file)
