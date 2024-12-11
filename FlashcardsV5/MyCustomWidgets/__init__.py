"""
Stores all files of Widgets created and/or modified by me

#### including...
- Universals:
    - TitleWidget
    - CustomFrame
    - CustomButton
    - CustomLabel
    - VerticalScrolledFrame
    - OptionWidget
---
- TopLevelManagers:
    - SubPage
    - TopLevelButton
---
- Miscellaneous:
    - QuestionButton
    - ResultWidget
    - KeyBindsWidget
"""

from .UniversalWidgets.titlewidget import TitleWidget
from .UniversalWidgets.customframe import CustomFrame
from .UniversalWidgets.custombutton import CustomButton
from .UniversalWidgets.customlabel import CustomLabel
from .UniversalWidgets.scrollableframe import VerticalScrolledFrame
from .UniversalWidgets.optionwidget import OptionWidget

from .TopLevelManagers.subpage import SubPage
from .TopLevelManagers.toplevelbutton import TopLevelButton

from .questionbutton import QuestionButton
from .resultwidget import ResultWidget
from .keybindswidget import KeyBindsWidget