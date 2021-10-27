from typing import Union, Optional, overload


def any_in_tag(gram: Union[set, str], parse) -> bool: pass
def inflect_noun(word: str, case: str, orig_form: Union[str, set, None]=None) -> Optional[str]: pass

@overload
def ChangeText(text: bytes) -> Optional[bytes]: pass
@overload
def ChangeText(text: str) -> Optional[str]: pass
