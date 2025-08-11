import inspect
import logging
import sys

from loguru import logger

RAW_EXT: tuple[str, str] = ("arw", "raw")


class InterceptHandler(logging.Handler):
    """標準のloggingモジュールのログをloguruにリダイレクトするハンドラー。

    このハンドラーは、標準のloggingモジュールで出力されたログメッセージを
    loguruのloggerにリダイレクトします。これにより、既存のloggingベースの
    ライブラリとloguruを統合して使用することができます。

    Source:
        https://github.com/Delgan/loguru?tab=readme-ov-file#entirely-compatible-with-standard-logging

    Examples:
        >>> import logging
        >>> logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
        >>> logging.info("This will be handled by loguru")
    """

    def emit(self, record: logging.LogRecord) -> None:
        """ログレコードをloguruに転送する。

        標準のloggingモジュールから受け取ったログレコードを解析し、
        適切な呼び出し元の情報を保持しながらloguruのloggerに転送します。

        Args:
            record: 標準のloggingモジュールからのログレコード。
                    レベル、メッセージ、例外情報などを含む。

        Note:
            このメソッドは、ログの呼び出し元を正確に特定するため、
            スタックフレームを遡って適切な深さを計算します。
        """
        # Get corresponding Loguru level if it exists.
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename: str = frame.f_code.co_filename
            is_logging: bool = filename == logging.__file__
            is_frozen: bool = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_loguru(verbose: bool) -> None:
    """loguruのロガーを設定し、標準loggingとの統合を行う。

    この関数は、loguruのデフォルトハンドラーを削除し、新しい設定で再構成します。
    標準のloggingモジュールのログをInterceptHandlerを通じてloguruに
    リダイレクトする設定も行います。

    Args:
        verbose: Trueの場合、ログレベルをDEBUGに設定。
                Falseの場合、ログレベルをINFOに設定。

    Examples:
        >>> configure_loguru(verbose=True)  # DEBUGレベルでログを出力
        >>> logger.debug("This debug message will be shown")

        >>> configure_loguru(verbose=False)  # INFOレベルでログを出力
        >>> logger.debug("This debug message will NOT be shown")
        >>> logger.info("This info message will be shown")

    Note:
        この関数は、アプリケーションの初期化時に一度だけ呼び出すことを推奨します。
        複数回呼び出すと、既存のハンドラーが削除され、新しいハンドラーで置き換えられます。
    """
    logger.remove()
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
    level_per_module: dict[str, str] = {"": "INFO"}
    if verbose:
        level_per_module = {"": "DEBUG"}
    logger.add(sys.stderr, diagnose=False, filter=level_per_module)  # type: ignore[arg-type]
