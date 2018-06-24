from nltk.corpus import wordnet
import string
import nltk
from nltk.stem.porter import *

from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
stemmer = PorterStemmer()

############LOCAL SERVER
#client = MongoClient()
#db = client['local']
#AAAI_IDF = db['AAAI_IDF']
#AAAI_stem_IDF = AAAI_IDF.find_one({'type':'stem'})['idf']


def maxSim(word_info,sentence_info,sim_method,word_min_len,model):
    word1 = word_info['word']
    word1_pos = word_info['pos']
    max_sim = 0

    for word_info in sentence_info:
        word2 = word_info['word']
        word2_pos = word_info['pos']
        current_sim = 0


        # (word1_pos!='R') and (word1_pos!='J') and (word2_pos!='R') and (word2_pos!='J') and
        if  (word1_pos ==word2_pos):# and (len(word1)>=word_min_len) and (len(word2)>=word_min_len):
            try:
                word1_synset = wordnet.synsets(word1)[0]
                word2_synset = wordnet.synsets(word2)[0]
                if sim_method=="path_similarity":
                    current_sim = word1_synset.path_similarity(word2_synset)
                elif sim_method == "lch_similarity":
                    current_sim = word1_synset.lch_similarity(word2_synset)
                elif  sim_method=="wup_similarity":
                    current_sim = word1_synset.wup_similarity(word2_synset)
                elif  sim_method=="res_similarity":
                    current_sim = word1_synset.res_similarity(word2_synset)
                elif  sim_method=="lin_similarity":
                    current_sim = word1_synset.lin_similarity(word2_synset)
                elif sim_method=='combined':
                    current_sim +=(
                    word1_synset.lch_similarity(word2_synset)+
                    word1_synset.lin_similarity(word2_synset))/2
                elif sim_method=='glove':
                    print ('to be imp')

                elif sim_method=='word2vec':
                    current_sim = model.similarity(word1,word2)

                if current_sim>max_sim:
                    max_sim  = current_sim
            except:
                if (word1==word2):
                    max_sim = 1#len(word1)
                    break
                #DoNothing = 0
        print(word1)
        print(word2)
        print(current_sim)
    return max_sim



def simT1T2(sentence1_info,sentence2_info,sim_method,word_min_len,model,idf_avg,idf,min_word_similarity_threshold):

    numerator = 0
    denominator = 1
    #selected_idf = {}
    #for word_info in sentence1_info:
    #    word1 = word_info['word']
    #    try:
    #        selected_idf[word1] = idf[word1]
    #    except:
    #        selected_idf[word1] = idf_avg

    #sorted_selected_idf = sorted(selected_idf.items(), key=operator.itemgetter(1))

    #used_idf = {}
    #num_to_use = (len(sorted_selected_idf) * (100 - percent_to_use)) / 100
    #for i in range(len(sorted_selected_idf)):
    #    if i < num_to_use:
    #        used_idf[sorted_selected_idf[i][0]] = 0
    #    else:
    #        used_idf[sorted_selected_idf[i][0]] = sorted_selected_idf[i][1]

    # print used_idf

    for word_info in sentence1_info:
        word1 = word_info['word']
        word1_pos = word_info['pos']
        try:
            word1_idf = idf[word1]
        except:
            word1_idf = idf_avg
            #print('here')


        sim_ =  maxSim({'word':word1,'pos':word1_pos},sentence2_info,sim_method,word_min_len,model)
        #print(sim_)

        if sim_>=min_word_similarity_threshold:
            numerator +=sim_*word1_idf
            denominator +=word1_idf

    return float(numerator)/denominator

def simTT(sentence1_info,sentence2_info,sim_method,word_min_len,model,idf_avg,idf,min_word_similarity_threshold):
    return 0.5*simT1T2(sentence1_info,sentence2_info,sim_method,word_min_len,model,idf_avg,idf,min_word_similarity_threshold)+0.5*simT1T2(sentence2_info,sentence1_info,sim_method,word_min_len,model,idf_avg,idf,min_word_similarity_threshold)



def create_sentence_info(sentence,remove_stop_words):
    exclude = set(string.punctuation)
    sentence_punctuation_removed = ''.join(ch for ch in sentence if ch not in exclude)
    if remove_stop_words:
        words = [i for i in sentence_punctuation_removed.split(' ') if i not in stop]
    else:
        words = sentence_punctuation_removed.split(' ')


    final_words = []
    for word in words:
        if word!='':
            type = nltk.pos_tag([word])[0][1][0]
            #word = stemmer.stem(word)
            final_words.append({'word':word,'pos':type})
    return final_words


def AAAI_Rada_Method(first_text,second_text,sim_method,word_min_len,model,idf_avg,idf,min_word_similarity_threshold):

    remove_stop_words = True
    first_sentence_info  = create_sentence_info(first_text,remove_stop_words)
    second_sentence_info  = create_sentence_info(second_text,remove_stop_words)

    return simTT(first_sentence_info,second_sentence_info,sim_method,word_min_len,model,idf_avg,idf,min_word_similarity_threshold)



#print (AAAI_Rada_Method("book paper","cat car","wup_similarity",0,0,1,{},0.4))

