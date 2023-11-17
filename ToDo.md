## Todo! 🌈

1. create method "failure files"

1. create a "exit button"

1.




## ChatGPT Code Review
> 코드리뷰를 진행해드리겠습니다.

- [x] 1. 코드의 import 부분에서 tkinter 라이브러리를 사용하고 있습니다. 이는 PyQt5와 함께 사용하지 않는 것이 좋습니다. 따라서 tkinter 라이브러리를 사용하지 않고 PyQt5의 QMessageBox를 사용하도록 수정하시는 것을 권장합니다.

- [x] 2. `MainWidget` 클래스에서는 `dropEvent` 메서드를 구현하지 않았는데, 이는 추상 메서드이므로 구현해주셔야 합니다.

- [x] 3. `FileMergeNDivide` 클래스에서는 `__init__` 메서드에서 중복된 코드가 있습니다. `super().__init__(parent)`을 호출하는 부분은 `MainWidget`에서 이미 호출하였기 때문에 제거하시는 것을 추천합니다.

- [x] 4. `update_title_widget` 메서드에서 `self.list_widget.count()`를 호출하여 `QListWidget`에 추가된 아이템의 수를 반환받고 있습니다. 이는 매우 비효율적인 방법입니다. `QListWidget`는 내부적으로 `countChanged` 시그널을 발생시키므로, 이 시그널을 받아서 바로 `title_widget`의 텍스트를 갱신하는 것이 더 나은 방법입니다.

- [x] 5. `_origin_to_combine_dic` 메서드에서 무한 루프를 사용하고 있습니다. 이는 위험한 방법이므로, `while` 문 대신 조건문을 사용하는 것이 좋습니다.

- [x] 6. `FileMergeNDivide` 클래스에서 `DESTINATION` 변수의 이름이 대문자로 작성되어 있습니다. Python의 관례상, 변수명은 모두 소문자로 작성하는 것이 좋습니다.

- [x] 7. `FileMergeNDivide` 클래스에서 `combine_files` 메서드에서 `try`-`except` 구문을 사용하여 예외 처리를 하고 있습니다. 이는 예외 처리 방식 중 가장 위험한 방식입니다. 이유는 모든 예외를 잡아서 처리하기 때문에, 예외가 발생했을 때 디버깅이 매우 어려워집니다. 따라서 가능한 구체적인 예외를 처리하는 것이 좋습니다.

- [x] 8. `FileMergeNDivide` 클래스에서 `combine_files` 메서드에서 리스트 컴프리헨션을 사용하여 리스트를 생성하는 부분이 있습니다. 이 코드는 매우 길고 복잡하므로, 가독성을 높이기 위해 여러 줄로 나누는 것이 좋습니다. 또한 이 코드는 파일을 처리하는 함수를 별도로 분리하여 사용하는 것이 좋습니다.



currentItemChanged(QListWidgetItem, QListWidgetItem)
currentRowChanged(int)
currentTextChanged(str)
itemActivated(QListWidgetItem)
itemChanged(QListWidgetItem)
itemClicked(QListWidgetItem)
itemDoubleClicked(QListWidgetItem)
itemEntered(QListWidgetItem)
itemPressed(QListWidgetItem)
itemSelectionChanged()