from .base import Question
from googleform import utils


def get_options(tree):
    xpath = (".//div[contains(@class, "
             "'freebirdThemedSelectOptionDarkerDisabled')]//span")

    # Ignore the first element, it is the "unselected" option
    option_elements = tree.xpath(xpath)[1:]

    return utils.eval_map(lambda x: x.text, option_elements)


class DropdownQuestion(Question):
    def __init__(self, question_tree):
        super().__init__(question_tree)

        self.options = get_options(self.tree)
        self._answer = None

    @staticmethod
    def is_this_question(tree):
        xpath = (".//div[contains(@class,"
                 "'freebirdFormviewerViewItemsSelectSelect')]")

        return bool(tree.xpath(xpath))

    def answer(self, option_name):
        self._answer = option_name

    def serialize(self):
        # Dropdown questions should only have one entry id
        entry_id = self.entry_ids[0]

        return {
            entry_id: self._answer
        }


question = DropdownQuestion
