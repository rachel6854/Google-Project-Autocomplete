from dataclasses import dataclass
from trie import searchCompletionsNodes, findAllMatchesOfNode


@dataclass
class AutoCompleteData:
    def __init__(self, sentence, source, offset, score):
        self.completed_sentence = sentence
        self.source_text = source
        self.offset = offset
        self.score = score


def organizeDataInClass(completed_sentences_, sentence, node):
    completed_sentence = completed_sentences_[sentence[0]][0]
    source_text = completed_sentences_[sentence[0]][1]
    offset = sentence[1]
    score = node[1]
    return AutoCompleteData(completed_sentence, source_text, offset, score)

def removeDuplicates(distinct_lst):
    done = set()
    result = []
    #sore distinct_list by offset
    distinct_lst.sort(key=lambda x:x.offset)
    for sentence in distinct_lst:
        if sentence.completed_sentence not in done:
            done.add(sentence.completed_sentence)
            result.append(sentence)
    return result

def choiceBestFiveSentences(completed_sentences, completionsNodes):
    result = []
    completed_sentences_ = completed_sentences
    for node in completionsNodes:
        currResult = []
        sentences = findAllMatchesOfNode(node[0])
        for sentence in sentences:
            currResult.append(organizeDataInClass(completed_sentences_, sentence, node))
        sentences.sort(key=lambda subSentence: completed_sentences_[subSentence[0]])
        result = removeDuplicates(result + currResult)[:5]
        if len(result) >= 5:
            break
    return result


def get_best_k_completions(trie, completed_sentences, prefix: str):
    completionsNodes = searchCompletionsNodes(trie["root"], prefix)
    completionsNodes.sort(key=lambda x: x[1], reverse=True)  # sort by score
    return choiceBestFiveSentences(completed_sentences, completionsNodes)
