# 導出核心類
from Chan import CChan
from ChanConfig import CChanConfig

# 導出枚舉類型
from Common.CEnum import DATA_SRC, KL_TYPE, AUTYPE, FX_TYPE

# 版本信息
__version__ = "1.0.0"

# 定義公開 API
__all__ = [
    # 核心類
    "CChan",
    "CChanConfig",
    
    # 枚舉類型
    "DATA_SRC",
    "KL_TYPE", 
    "AUTYPE",
    "FX_TYPE",
    
    # 版本信息
    "__version__",
    "__author__",
]