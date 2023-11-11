import nltk
import regex as re
from collections import Counter



class Concordancer():
    left_context_length = 50
    right_context_length = 50
      
    def __init__(self):
        super().__init__()
        self.line_of_token_list = []

    def read_tokens(self, file_name):
        token_list = []
        input_text = open(file_name, "r")
        for line in input_text.readlines():
            token_list = nltk.wordpunct_tokenize(line)
            self.line_of_token_list.append(token_list)
        input_text.close()
    
    def find_concordance(self, query, num_words):
        indices = {}        #A dict of lists: Id = line number, values in list = indices where query found
        concordance_list = []
        
        for line_id in range(len(self.line_of_token_list)):
            current_line_list = [index for index in range(len(self.line_of_token_list[line_id])) if self.line_of_token_list[line_id][index] == query]              
            if current_line_list:
                indices.update({line_id:current_line_list})
        
        if not indices:      #If the dict is empty then throw an error and return
            print("Query not found…")
            return
        
        for line_id in indices.keys():          #Iterate on each line
            
            for index in indices[line_id]:      #Iterate on each match
                buffer = []
                for space in range(num_words):
                    buffer.append(" ")
                    
                buffer.append(query)        
                                
                for space in range(num_words):
                    buffer.append(" ")
                
                #At this point buffer looks like: [" ", " ", " ", ... query, " ", " ", " "...]
                #Query index will always = num_words 0, 1, query(2), 3, 4 ---> Num_ words = 2 
                
                for buffer_id_diff in range(1, min(num_words, index) +1 ):
                    buffer[num_words - buffer_id_diff] = self.line_of_token_list[line_id][index - buffer_id_diff]

                for buffer_id_diff in range(1, min(len(self.line_of_token_list[line_id][index:]), num_words + 1), 1):
                    buffer[num_words + buffer_id_diff] = self.line_of_token_list[line_id][index + buffer_id_diff]

                concordance_list.append(buffer)
                    
            
        for list_of_words in concordance_list:  #Get each list of suitable context seperately
            first_half = " ".join(list_of_words[0:num_words])   #the first [num_words] words (not including keyword)
            second_half = " ".join(list_of_words[num_words +1:]) #The last [num_words] words (not including keyword)
            
            while len(first_half) > self.left_context_length:
                first_half = first_half[1:]
            
            while len(first_half) < self.left_context_length:        #If there aren't enough chars before the query word, add more
                first_half = " " + first_half
            
            while len(second_half) > self.right_context_length:
                second_half = first_half[:-1]
                            
            while len(second_half) < self.right_context_length:
                second_half += " "
                        
            print(f"{first_half} {query} {second_half}")
        return    


    def find_concordance_ngram(self, ngram_query, num_words):
        """
        Insert your docstring here
        """
        pass            

    def compute_bigram_stats(self, query, output_file_name):
        stats_file = open(str(output_file_name), "w")
        bigram_list = []

        
        for line in self.line_of_token_list:
            for word_id in range(len(line) - 1):    # -1 because No need to check the last word
                if line[word_id] != query:          #If not query, move on to next word
                    continue
                if re.fullmatch(r"[^\w\s]+",line[word_id + 1]):      #if next token is punctuation then ignore and move on
                    continue
                
                bigram_list.append(f"{line[word_id]} {line[word_id+1]}") 
        
        bigram_list = Counter(bigram_list).most_common()   #returns a list of tuples where index[0] is the value, index[1] is the frequency as int
        
        for bigram_freq_tuple in bigram_list:
            stats_file.write(f"{str(bigram_freq_tuple[0])} {str(bigram_freq_tuple[-1])}\n")
        stats_file.close()        


        
