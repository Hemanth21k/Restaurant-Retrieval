


#This was implemented based on Snowball (Porter2) algorithm
#link http://snowball.tartarus.org/algorithms/english/stemmer.html


class PorterStemmer2:
    def isVowel(self,letter):
        vowels = ['a','e','i','o','u','y']
        if letter in vowels:
            return True
        else:
            return False
    def isDouble(self,seq):
        doubles = ['bb','dd','ff','gg','mm','nn','pp','rr','tt']
        if seq in doubles:
            return True
        else:
            return False
    def isLiEnd(self,letter):
        li = ['c','d','e','g','h','k','m','n','r','t']
        if letter in li:
            return True
        else:
            return False
    def getR1(self,word):
        R1 = ""
        for i in range(len(word)):
            if not self.isVowel(word[i]):
                if i > 0 and self.isVowel(word[i-1]):
                    R1 = word[i+1:]
                    break
        return R1
    def getR2(self,word):
        R1 = self.getR1(word)
        R2 = self.getR1(R1)
        return R2
    def hasShortSyllable(self,word):
        checkIn = ['w','x','Y']
        for i in range(len(word)):
            if self.isVowel(word[i]):
                if i==0 and i+1<len(word):
                    if not self.isVowel(word[i+1]):
                        return True
                elif i>0 and i<len(word)-1:
                    if not self.isVowel(word[i-1]) and not self.isVowel(word[i+1]):
                        if word[i+1] not in checkIn:
                            return True
                else:
                    pass
        return False
        
    def isShort(self,word):
        r1 = self.getR1(word)
        if r1 == "":
            if len(word) >=3:
                if self.hasShortSyllable(word[len(word)-3:]):
                    return True
                else:
                    return False
            else:
                if self.hasShortSyllable(word[len(word)-2:]):
                    return True
                else:
                    return False 
        else:
            return False
    def markVowelasCons(self,word):
        out = list(word)
        for i in range(len(word)):
            if i == 0  and out[i] == 'y':
                out[i] = 'Y'
            elif i>0 and out[i] == 'y' and self.isVowel(out[i-1]):
                out[i] = 'Y'
            else:
                continue
        return ''.join(out)

    def removeList(self,i,l,wlist):
        while i < l:
            wlist.pop(i)
            l-=1
            
    def endsWith(self,word,suffix):
        if len(word) >= len(suffix):
            if word[len(word)-len(suffix):] == suffix:
                return True
            else:
                return False
        else:
            return False
        
    def step0(self,wordlist):
        l = len(wordlist)
        i = l-3
        while i < l:
            if wordlist[i] == '\'':
                if i == l-1:
                    wordlist.pop(i)
                    l-=1
                else:
                    if wordlist[i+1] == 's':
                        wordlist.pop(i+1)
                        wordlist.pop(i)
                        l-=2
            else:
                i+=1

    def step1a(self,wlist):
        temp = "".join(wlist)
        l = len(wlist)
        if self.endsWith(temp,"sses"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(temp,"ied") or self.endsWith(temp,"ies"):
            i = len(wlist)-2
            if l <= 4:
                i+=1
            self.removeList(i,l,wlist)
        elif self.endsWith(temp,"ss") or self.endsWith(temp,"us"):
            pass
        elif temp[-1] == 's':
            r = 0
            for i in range(len(wlist)-2):
                if self.isVowel(wlist[i]):
                    r = 1
            if r == 1:
                wlist.pop(len(wlist)-1)
        else:
            pass
        
    def checkAfter1b(self,wlist):
        word = "".join(wlist)
        last2 = word[len(word)-2:]
        if last2 == "at" or last2 == "bl" or last2 == "iz":
            wlist.append('e')
        elif self.isDouble(last2):
            wlist.pop()
        elif self.isShort(word):
            wlist.append('e')
        else:
            pass
    
    def hasVowel(self,prefix):
        for i in range(len(prefix)):
            if self.isVowel(prefix[i]):
                return True
        return False
    def step1b(self,wlist):
        word = "".join(wlist)
        r1 = self.getR1(word)
        i = len(wlist)
        l = len(wlist)
        if self.endsWith(r1,"eed"):
            self.removeList(i-1,l,wlist)
        elif self.endsWith(r1,"eedly"):
            self.removeList(i-3,l,wlist)
        elif self.endsWith(word,"ed") and self.hasVowel(word[:l-2]):
            self.removeList(i-2,l,wlist)
            self.checkAfter1b(wlist)
        elif self.endsWith(word,"edly") and self.hasVowel(word[:l-4]):
            self.removeList(i-4,l,wlist)
            self.checkAfter1b(wlist)
        elif self.endsWith(word,"ing") and self.hasVowel(word[:l-3]):
            self.removeList(i-3,l,wlist)
            self.checkAfter1b(wlist)
        elif self.endsWith(word,"ingly") and self.hasVowel(word[:l-5]):
            self.removeList(i-5,l,wlist)
            self.checkAfter1b(wlist)
        else:
            pass

    def step1c(self,wlist):
        if len(wlist) > 2:
            for i in range(2,len(wlist)):
                if wlist[i] == 'y' or wlist[i] == "Y":
                    if not self.isVowel(wlist[i-1]):
                        wlist[i] = 'i'
                    else:
                        pass
                else:
                    pass
        else:
            pass
        
                
                
    def step2(self,wlist):
        word = "".join(wlist)
        r1 = self.getR1(word)
        l = len(wlist)
        if self.endsWith(r1,"tional"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"enci"):
            wlist[l-1] = 'e'
        elif self.endsWith(r1,"anci"):
            wlist[l-1] = 'e'
        elif self.endsWith(r1,"abli"):
            wlist[l-1] = 'e'
        elif self.endsWith(r1,"entli"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"izer"):
            self.removeList(l-1,l,wlist)
        elif self.endsWith(r1,"ization"):
            self.removeList(l-5,l,wlist)
            wlist.append('e')
        elif self.endsWith(r1,"ational"):
            self.removeList(l-5,l,wlist)
            wlist.append('e')
        elif self.endsWith(r1,"ation"):
            self.removeList(l-3,l,wlist)
            wlist.append('e')
        elif self.endsWith(r1,"ator"):
            self.removeList(l-2,l,wlist)
            wlist.append('e')
        elif self.endsWith(r1,"alism"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r1,"aliti"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r1,"alli"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"fulness"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r1,"ousli"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"ousness"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r1,"iveness"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r1,"iviti"):
            self.removeList(l-3,l,wlist)
            wlist.append('e')
        elif self.endsWith(r1,"biliti"):
            self.removeList(l-5,l,wlist)
            wlist.extend(['l','e'])
        elif self.endsWith(r1,"bli"):
            wlist[l-1] = 'e'
        elif self.endsWith(r1,"ogi"):
            if wlist[l-4] == 'l':
                wlist.pop()
        elif self.endsWith(r1,"fulli") or self.endsWith(r1,"lessli"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"li") and self.isLiEnd(wlist[l-3]):
            self.removeList(l-2,l,wlist)
        else:
            pass
            
    def step3(self,wlist):
        word = "".join(wlist)
        r1 = self.getR1(word)
        r2 = self.getR2(word)
        l = len(wlist)
        if self.endsWith(r1,"tional"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"ational"):
            self.removeList(l-5,l,wlist)
            wlist.append('e')
        elif self.endsWith(r1,"alize"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r1,"icate") or self.endsWith(r1,"iciti"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r1,"ical"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r1,"ful"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r1,"ness"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r2,"ative"):
            self.removeList(l-5,l,wlist)
        else:
            pass
    def step4(self,wlist):
        r2 = self.getR2("".join(wlist))
        l = len(wlist)
        if self.endsWith(r2,"al"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r2,"ance"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r2,"ence"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r2,"er"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r2,"ic"):
            self.removeList(l-2,l,wlist)
        elif self.endsWith(r2,"able"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r2,"ible"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r2,"ant"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ement"):
            self.removeList(l-5,l,wlist)
        elif self.endsWith(r2,"ment"):
            self.removeList(l-4,l,wlist)
        elif self.endsWith(r2,"ent"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ism"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ate"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"iti"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ous"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ive"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ize"):
            self.removeList(l-3,l,wlist)
        elif self.endsWith(r2,"ion"):
            if l > 3:
                if wlist[l-4] == 's' or wlist[l-4] == 't':
                    self.removeList(l-3,l,wlist)
        else:
            pass
    def step5(self,wlist):
        word = "".join(wlist)
        l = len(wlist)
        r1 = self.getR1(word)
        r2 = self.getR2(word)
        if self.endsWith(r2,'e'):
            wlist.pop()
        elif self.endsWith(r2,'l') and wlist[l-2] == 'l':
            wlist.pop()
        elif self.endsWith(r1,'e'):
            if l>3:
                if not self.hasShortSyllable(word[l-4:l-1]):
                    wlist.pop()
            else:
                if not self.hasShortSyllable(word[l-3:l-1]):
                    wlist.pop()
        else:
            pass
            
        
    def stem(self,word):
        if len(word) <= 2:
            return word
        if word[0] == '\'':
            word = word[1:]
        out = list(word)
        self.step0(out)
        self.step1a(out)
        self.step1b(out)
        self.step1c(out)
        self.step2(out)
        self.step3(out)
        self.step4(out)
        self.step5(out)
        final = "".join(out)
        
        return final.lower()
        
            
                
