from pathlib import Path

import pytest

from lrutility.xmp.XMPParser import XMPParser


class TestXmpParser:
    """XMPパーサーのテストクラス。"""

    def setup_method(self) -> None:
        """各テストメソッドの前に実行される。"""
        self.parser = XMPParser()

    def test_rating_xmp(self) -> None:
        """rating_1.xmpからRawImageNameとRatingを正しく取得できることを確認。"""
        xmp_file = Path("tests/assets/rating_1.xmp")
        metadata = self.parser.parse(xmp_file)

        # RawImageNameの確認
        assert metadata.camera_raw_settings.raw_file_name == "rating_1.ARW"

        # Ratingの確認（1が設定されている）
        assert metadata.xmp_info.rating == 1

    def test_not_rating_xmp(self) -> None:
        """not_rating.xmpからRawImageNameを取得し、Ratingがないことを確認。"""
        xmp_file = Path("tests/assets/not_rating.xmp")
        metadata = self.parser.parse(xmp_file)

        # RawImageNameの確認
        assert metadata.camera_raw_settings.raw_file_name == "not_rating.ARW"

        # Ratingの確認（設定されていないのでNone）
        assert metadata.xmp_info.rating is None

    def test_file_not_found(self) -> None:
        """存在しないファイルに対してFileNotFoundErrorが発生することを確認。"""
        non_existent_file = Path("tests/assets/non_existent.xmp")
        with pytest.raises(FileNotFoundError, match="XMP file not found"):
            self.parser.parse(non_existent_file)

    def test_parse_datetime(self) -> None:
        """parse_datetimeメソッドのテスト。"""
        # 正常な日時文字列
        result = XMPParser.parse_datetime("2024-01-01T12:00:00Z")
        assert result is not None
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 1

        # Noneの場合
        assert XMPParser.parse_datetime(None) is None

        # 空文字列の場合
        assert XMPParser.parse_datetime("") is None

        # 不正な形式の場合
        assert XMPParser.parse_datetime("invalid") is None

    def test_parse_fraction(self) -> None:
        """parse_fractionメソッドのテスト。"""
        # 分数形式
        assert XMPParser.parse_fraction("1/2") == 0.5
        assert XMPParser.parse_fraction("100/10") == 10.0

        # 整数・小数形式
        assert XMPParser.parse_fraction("3.14") == 3.14
        assert XMPParser.parse_fraction("42") == 42.0

        # Noneの場合
        assert XMPParser.parse_fraction(None) is None

        # 空文字列の場合
        assert XMPParser.parse_fraction("") is None

        # ゼロ除算の場合
        assert XMPParser.parse_fraction("1/0") is None

        # 不正な形式の場合
        assert XMPParser.parse_fraction("invalid") is None
