class MatrixSyntaxError(Exception):
    pass


def self_eval(A):
    
    if A.find('j') != -1:
        if A.find('j') == 0:
            A = A.replace('j','1j',1)            
        elif A.find('-j') != -1:
            A = A.replace('-j','-1j',1)
        elif A.find('+j') != -1:
            A = A.replace('+j','+1j',1)
        elif A.find('*j') != -1:
            A = A.replace('*j','*1j',1)
        try: 
            Aval = eval(A)
        except:
            raise MatrixSyntaxError    
    else:
        try:
            Aval = eval(A)
        except:
            raise MatrixSyntaxError    
    if Aval == 0:
        return 0
    elif isinstance(Aval,int):
        return Aval
    elif isinstance(Aval,float):
        if Aval == int(Aval):
            return int(Aval)
        else:
            return Aval
    elif isinstance(Aval,complex):
        Aval_real = self_eval(str(complex(Aval).real))
        Aval_imag = self_eval(str(complex(Aval).imag))
        if Aval_real == 0:
            return complex(0,Aval_imag)
        elif Aval_imag == 0:
            return Aval_real
        else:
            return Aval
    else:
        raise MatrixSyntaxError
        

def Str2Mat(s):

    s = s.replace(' ','')
    if s[0] != '[' or s[-1] != ']':    
        raise MatrixSyntaxError
    s = s.replace('[','',1).replace(']','',1)
    stri = s.split(';')
    mat = []
    if stri != ['']:
        for i in range(len(stri)):
            mat.append([])
            strii = stri[i].split(',')
            for j in range(len(strii)):
                mat[i].append(self_eval(strii[j]))
        line = len(mat[0])
        for i in mat:
            if line != len(i):
                raise MatrixSyntaxError
    return mat	

def Mat2StrStandard(A):

    StaString = '['
    if A != []:
        line = len(A[0])    
        for i in range(len(A)):
            for j in range(line):
                ele_string = str(self_eval(str(A[i][j]))).strip('()')
                StaString = StaString + ele_string + ','
            StaString = StaString.rstrip(',') + ';'
    StaString = StaString.rstrip(';') + ']'
    return StaString
	
	
def MatAdd(A, B):

    Sum = []
    for i in range(len(A)):
        Sum.append([])
        for j in range(len(A[0])):
            Sum[i].append(A[i][j] + B[i][j])	
    return Sum

def MatSub(A, B):

    Sub = []
    for i in range(len(A)):
        Sub.append([])
        for j in range(len(A[0])):
            Sub[i].append(A[i][j] - B[i][j])
    return Sub
def MatScalarMul(A, c):

    Mul = []
    for i in range(len(A)):
        Mul.append([])
        for j in range(len(A[0])):
            Mul[i].append(A[i][j] * c)
    return Mul
    
def MatTransposition(A):

    if A == []:
        return A
    else:
        rowT = len(A)
        lineT = len(A[0])
        Tran = []
        for i in range(lineT):
            Tran.append([])
            for j in range(rowT):
                Tran[i].append(A[j][i])
        return Tran

def MatEq(A, B):

    if A == B:
        return True
    else:
        return False

def determinanta(A):
    if len(A) == 0:
        return 1
    elif len(A) == 1:
        return A[0][0]
    elif len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    elif len(A) > 2:          
        det = 0        
        for i in range(len(A)):
            Matx = []        
            for j in range(len(A) - 1):
                Matx.append([])
                for k in range(len(A)):
                    if i != k:
                        Matx[j].append(A[j+1][k])    
            det = det + A[0][i] * ((-1) ** (i % 2)) * determinanta(Matx)
        return det
    else:
        raise MatrixSyntaxError


 
class Matrix(object):

    def __init__(self,s):
        self.s = s
        self.l = Str2Mat(self.s)
        self.row = len(self.l)
        if self.l != []:
            self.line = len(self.l[0])
        else:
            self.line = 0
    
    def __setitem__(self,key,value):
        if self.l == []:
            raise MatrixSyntaxError        
        elif isinstance(key, int):            
            if key > self.row or value.line != self.line or not isinstance(value, Matrix):
                raise MatrixSyntaxError
            else:                                    
                self.l[key] = value.l[0]
        elif isinstance(key,tuple):
            if len(key) == 2:            
                if isinstance(key[0], slice) and isinstance(key[1], slice):            
                    try:
                        row_cut = [i for i in range(self.row)][key[0]]
                        line_cut = [i for i in range(self.line)][key[1]] 
                        for i in range(len(row_cut)):
                            for j in range(len(line_cut)):
                                self.l[row_cut[i]][line_cut[j]] = value.l[i][j] 
                    except:
                        raise MatrixSyntaxError
                elif isinstance(key[0], int) and isinstance(key[1], int) and key[0] <= self.row and key[1] <= self.line:
                    try: 
                        self.l[key[0]][key[1]] = self_eval(str(value))
                    except:
                        raise MatrixSyntaxError                
                else:
                    raise MatrixSyntaxError
            else:
                raise MatrixSyntaxError
        else:
            raise MatrixSyntaxError

    def __getitem__(self,key):            
        if self.l == []:
            raise MatrixSyntaxError
        elif isinstance(key, int):
            if key > self.row:
                raise MatrixSyntaxError
            else:                                                    
                StrValue = []
                StrValue.append(self.l[key])               
                return Mat2StrStandard(StrValue)
        elif isinstance(key,tuple):
            if len(key) == 2:             
                if isinstance(key[0], slice) and isinstance(key[1], slice):            
                    row_cut = [i for i in range(self.row)][key[0]]
                    line_cut = [i for i in range(self.line)][key[1]]                   
                    l_cut = []                
                    for i in range(len(row_cut)):
                        l_cut.append([])                    
                        for j in range(len(line_cut)):
                            l_cut[i].append(self.l[row_cut[i]][line_cut[j]])
                    return Mat2StrStandard(l_cut)
                elif isinstance(key[0], int) and isinstance(key[1], int) and key[0] <= self.row  and key[1] <= self.line:
                    return self.l[key[0]][key[1]]
                else:
                    raise MatrixSyntaxError
            else:
                raise MatrixSyntaxError
        else:
            raise MatrixSyntaxError 

    def __add__(self,other):
        if self.line == other.line and self.row == other.row and isinstance(self,Matrix) and isinstance(other,Matrix):
            return Matrix(Mat2StrStandard(MatAdd(self.l,other.l))) 
        else:
            raise MatrixSyntaxError 

    def __sub__(self,other):
        if self.line == other.line and self.row == other.row and isinstance(self,Matrix) and isinstance(other,Matrix):
            return Matrix(Mat2StrStandard(MatSub(self.l,other.l))) 
        else:
            raise MatrixSyntaxError 

    def __mul__(self,other):
        if isinstance(other, Matrix) and isinstance(self, Matrix):
            if self.line == other.row:
                if self.l == other.l == []:
                    return Matrix('[]')
                else:
                    Outcome = []                    
                    for i in range(self.row):
                        Outcome.append([])
                        for j in range(other.line):
                            Aij = 0
                            for k in range(self.line):
                                Aij = Aij + self.l[i][k] * other.l[k][j]
                            Outcome[i].append(Aij)
                    return Matrix(Mat2StrStandard(Outcome))
            else:
                raise MatrixSyntaxError
        else:
            others = self_eval(str(other))
            return Matrix(Mat2StrStandard(MatScalarMul(self.l, others)))

    def __truediv__(self,other):
        if other == 0:
            raise MatrixSyntaxError
        else:
            Div = []
            for i in range(self.row):
                Div.append([])
                for j in range(self.line):
                    Div[i].append(self.l[i][j] / other)
            return  Matrix(Mat2StrStandard(Div))

    def __neg__(self):
        Neg = []
        for i in range(self.row):
            Neg.append([])
            for j in range(self.line):
                 Neg[i].append(-self.l[i][j])
        return  Matrix(Mat2StrStandard(Neg))

    def __pow__(self,other):
        if isinstance(other,int) and other >= 1:
            if other == 1:
                return self
            else:
                for i in range(other):
                    return self * (self ** (other-1))
        else:
            raise MatrixSyntaxError   

    def __eq__(self,other):
        if isinstance(self,Matrix) and isinstance(other,Matrix):
            return MatEq(self.l, other.l)
        else:
            raise MatrixSyntaxError

    def isIdentity(self):
        if self.l != []:
            if self.line == self.row:
                for i in range(self.row):
                    for j in range(self.line):
                        if i != j and self.l[i][j] != 0:
                            return False
                        elif i == j and self.l[i][j] != 1:
                            return False
                return True            
            else:
                return False
        else:
            return True

    def isSquare(self):
        if self.row == self.line:
            return True
        else:
            return False
    
    def transposition(self):
        return Matrix(Mat2StrStandard(MatTransposition(self.l)))


    def determinant(self):
        if self.isSquare:    
            return determinanta(self.l)
          
    def inverse(self):
        if self.isSquare:
            detx = []            
            if self.row == 1:
                detx.append([])                
                detx[0] = self.l[0][0]
            elif self.row == 2:
                detx.append([])
                detx.append([])                
                detx[0] = [self.l[1][1],-self.l[1][0]]
                detx[1] = [-self.l[0][1],self.l[0][0]]
            elif self.row > 2:
                for i in range(self.row):
                    detx.append([])                    
                    for j in range(self.row):
                        detxx = []
                        x = -1
                        for k in range(self.row):
                            if k != i:
                                x = x + 1                                
                                detxx.append([])                        
                                for p in range(self.row):
                                    if j != p:
                                        detxx[x].append(self.l[k][p])                                    
                                    
                        detx[i].append(determinanta(detxx) * (-1) ** (i + j))

            detx_trans = MatTransposition(detx)
            detx_det = determinanta(self.l)
            detx_matrix = Matrix(Mat2StrStandard(detx_trans))
            return detx_matrix / detx_det
        else:
            raise MatrixSyntaxError

    def __str__(self):
        return Mat2StrStandard(self.l)
