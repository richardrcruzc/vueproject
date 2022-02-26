import requests


def define_word(input_word):
    print(input_word)
    resp = requests.get('http://prpm.dbp.gov.my/Search?k='+input_word.replace(" ", "+"))
    if resp.status_code == requests.codes.ok:
        test_code = resp.text.find("Carian kata tiada di dalam kamus terkini.")

        if test_code == -1:
            word_definition = resp.text.split('Definisi', 1)[-1].split('</div>')[0][7:]
            word_definition = word_definition.replace('&nbsp;', ' ').replace('<b>', '\n').replace('</b>', '')
            #print(word_definition)

            return {'status': 0, 'definition': word_definition}
        else:
            # Cannot find word
            return {'status': 1, 'error': 1}

    return {'status': 1, 'error': 0}