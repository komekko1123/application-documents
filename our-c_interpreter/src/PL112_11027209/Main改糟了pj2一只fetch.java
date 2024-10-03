package PL112_11027209;
import java.util.*;
import java.lang.Exception;
import CYICE.*;

abstract class G{   
  public static int s_utestnum; // debug用
  public static int s_quit; // quit用的
  public static ICEInputStream sin = null;
  public static ArrayList<Identifier> s_DefineTable = null; // 放定義字的表，因為parser跟execute都會用到
  // 上面是I/O  下面是ENUM區
  
  public final static int EOF = 61396;
  public final static int IDENT = 1;
  public final static int CONSTANT = 2;
  public final static int INT = 3;
  public final static int FLOAT = 4;
  public final static int CHAR = 5;
  public final static int BOOL = 6;
  public final static int STRING = 7; 
  public final static int VOID = 8; 
  public final static int IF = 9; 
  public final static int ELSE = 10;
  public final static int WHILE = 11; 
  public final static int DO = 12; 
  public final static int RETURN = 13; 
  public final static int LSP = 14; // SMALL P (
  public final static int RSP = 15; 
  public final static int LMP = 16; // MID P [
  public final static int RMP = 17;
  public final static int LBP = 18; // BIG P{
  public final static int RBP = 19; 
  public final static int PLUS = 20;  // +
  public final static int MINUS = 21; // -
  public final static int STAR = 22;  // *
  public final static int DIV = 23;   // /
  public final static int PERCENT = 24; // %
  public final static int HAT = 25; // ^
  public final static int GT   = 26; // greater than >
  public final static int LT = 27;  // lower than <
  public final static int GE = 28; // greater equal >=
  public final static int LE = 29; // lower equal <=
  public final static int EQ = 30; // ==
  public final static int NEQ = 31; // !=
  public final static int HALF_AND = 32; // &
  public final static int HALF_OR = 33;  // |
  public final static int HALF_EQ = 34; // =
  public final static int HALF_NEQ = 35; // !
  public final static int AND = 36; // &&
  public final static int OR = 37; // ||
  public final static int PE = 38; // +=
  public final static int ME = 39; // -=
  public final static int TE = 40; // *=
  public final static int DE = 41; // /=
  public final static int RE = 42; // %=
  public final static int PP = 43; // ++
  public final static int MM = 44; // -- 
  public final static int RS = 45; // >> 
  public final static int LS = 46; // <<
  public final static int SC = 47 ; // ;
  public final static int CM = 48; // , COMMA 
  public final static int QM = 49; // ? QUESTION MARK
  public final static int CL = 50; // : COLON  
  public final static int COUT = 51; // COUT
  public final static int CIN = 52; // CIN
  public final static int UNKNOWN = 16926; // 未知NODE
  
  public static void Init() throws Throwable {
    // sin = new ICEInputStream( );  // 這行可以改要讀什麼txtttttttttt
    sin = new ICEInputStream( "test2.txt" );  // 這行可以改要讀什麼txtttttttttt
    s_DefineTable = new ArrayList<Identifier>();
    s_quit = 0;
  } // Init()
  
  public static boolean CheckIDInTable( String str ) throws Throwable {
    for ( int i = 0 ; i < s_DefineTable.size() ; i++ ) {
      if ( s_DefineTable.get( i ).mvalue.equals( str ) ) // 有相同的字代表已被定義 
        return true;
    } // for
    
    return false;
  } // CheckIDInTable()
  
  public static void UpdateIDInTable( Identifier Ide ) throws Throwable {
    if ( CheckIDInTable( Ide.mvalue ) == true ) {
      for ( int i = 0 ; i < s_DefineTable.size() ; i++ ) { // 找到值並更改
        if ( Ide.mvalue.equals( s_DefineTable.get( i ).mvalue ) ) // 找到同字串
          s_DefineTable.set( i, Ide );  
      } // for
    } // if
    
    else // 只接放進去
      s_DefineTable.add( Ide );  
  } // UpdateIDInTable() 
  
  public static Identifier GetIDInTable( String str ) throws Throwable {
    Identifier ide = null;
    for ( int i = 0 ; i < s_DefineTable.size() ; i++ ) { // 找到值並更改
      if ( str.equals( s_DefineTable.get( i ).mvalue ) ) // 找到同字串
        ide = s_DefineTable.get( i );
    } // for
    
    return ide;
  } // GetIDInTable() 
  
  
  public static void CYPrint( String str ) throws Throwable {
    byte[] binary = str.getBytes( "Big5" );
    System.out.write( binary, 0, binary.length );
  } // CYPrint()
  
  public static void ErrorPrint( boolean a, boolean b, boolean c, Token t  ) {
    if ( a == true ) {
      System.out.print( "> Unrecognized token with first char : " + '\'' + t.mvalue + '\'' + '\n' );
      return;
    } // if
    else if ( b == true ) {
      System.out.print( "> Unexpected token : " + '\'' + t.mvalue + '\'' + '\n' );
    } // else if

    else if ( c == true ) {
      System.out.print( "> Undefined identifier : " + '\'' + t.mvalue + '\'' + '\n' );
    } // else if
  } // ErrorPrint() 
} // class G


class Token {
  public int mtype;
  public String mvalue;
  public int mline;
  public int mcolumn;
  Token() {
    this.mtype = 0 ;
    this.mcolumn = 0;
    this.mline = 0;
    this.mvalue = new String();
  } // Token()
  
  Token( int type, String value, int line, int column ) {
    this.mtype = type;
    this.mvalue = value;
    this.mline = line;
    this.mcolumn = column;
  } // Token()
} // class Token

class Identifier {
  public int mtype;
  public String mvalue;
  public double mnumvalue;
  public String mcheck; // check int or double
  Identifier() {
    this.mtype = 0;
    this.mvalue = new String();
    this.mnumvalue = 0;
    this.mcheck = new String();
  } // Identifier()
  
  Identifier( int type, String value, double numvalue, String mcheck ) {
    this.mtype = type;
    this.mvalue = value;
    this.mnumvalue = numvalue;
    this.mcheck = mcheck;
  } // Identifier()  
} // class Identifier





class SCANNER {
  public LinkedHashMap<String,String> mLHM = new LinkedHashMap<String,String>();
  public ArrayList<Token> mTokenlist = new ArrayList<Token>(); // 放每個token 用完刪除remove_all
  public Token mnow_token = null;
  public int m_tokenNum = 0 ; // token
  public int ms_lineNumber = 1;
  public int ms_columnNumber = 1;
  public char m_nextchar = '\0';
  public Token FetchToken() throws Throwable {
    if (mnow_token != null) {
      Token t = new Token( mnow_token.mtype, mnow_token.mvalue, 
                           mnow_token.mline, mnow_token.mcolumn  ); 
      mnow_token = null;
      return t;
    } // if
    
    char first = '\0';
    String str = new String(); 
    if ( IsSpace( m_nextchar ) ) // 不是whitespace 有包括\0
      m_nextchar = GetNextNonWhiteSpaceChar(); // 拿下一個非white的token
    first = m_nextchar;
    PeekNextChar();
    int check = 0;
    str = str + first;  
    if ( first == '\0' ) // EOF了
      return new Token( G.EOF, "", ms_lineNumber, ms_columnNumber  );   
    else if ( IsLetter( first ) ) { // 字母開頭
      while ( IsLetter( this.m_nextchar ) || IsNum( this.m_nextchar ) || m_nextchar == '_'   ) {
        first = m_nextchar; // 字母的話可以是字母數字下底線----是這三者的話
        str = str + first;
        PeekNextChar();   
      } // while
      
      if ( str.equals( "int" ) )
        return new Token( G.INT, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "float" ) )
        return new Token( G.FLOAT, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "char" ) )
        return new Token( G.CHAR, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "bool" ) )
        return new Token( G.BOOL, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "string" ) )
        return new Token( G.STRING, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "void" ) )
        return new Token( G.VOID, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "if" ) )
        return new Token( G.IF, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "else" ) )
        return new Token( G.ELSE, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "while" ) )
        return new Token( G.WHILE, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "do" ) )
        return new Token( G.DO, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "return" ) )
        return new Token( G.RETURN, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "cin" ) )
        return new Token( G.CIN, str, ms_lineNumber, ms_columnNumber  );    
      else if ( str.equals( "cout" ) )
        return new Token( G.COUT, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "true" ) )
        return new Token( G.CONSTANT, str, ms_lineNumber, ms_columnNumber  );  
      else if ( str.equals( "false" ) )
        return new Token( G.CONSTANT, str, ms_lineNumber, ms_columnNumber  );  
      else
        return new Token( G.IDENT, str, ms_lineNumber, ms_columnNumber  ); 
    } // else if
    
    else if ( IsNum( first ) ) { // 有可能是數字or小數
      if ( m_nextchar == '.' )
        check = check + 1;
      while ( ( IsNum( this.m_nextchar ) || this.m_nextchar == '.' ) && check < 2 ) { 
        first = m_nextchar; // 數字的話可以是.或是數字且只能有一個小數點----是這二者的話
        str = str + first;
        PeekNextChar();   
        if ( this.m_nextchar == '.' ) // 有一個點點 不能超過兩個
          check = check + 1; 
      } // while
      
      return new Token( G.CONSTANT, str, ms_lineNumber, ms_columnNumber  );
    } // else if 
    
    else if ( first == '.' ) { // ..後面只能是數字
      if ( ! IsNum( this.m_nextchar ) ) // 下一個一定要是數字才對
        return new Token( G.UNKNOWN, str, ms_lineNumber, ms_columnNumber  );
      while (  IsNum( this.m_nextchar ) ) { // 數字的話可以是.或是數字且只能有一個小數點
        first = m_nextchar; // 是這三者的話
        str = str + first;
        PeekNextChar();        
      } // while
      
      return new Token( G.CONSTANT, str, ms_lineNumber, ms_columnNumber  );
    } // else if
    
    else if ( first == '+' ) { // 符號
      if ( this.m_nextchar == '+' ) {
        PeekNextChar();
        return new Token( G.PP, "++", ms_lineNumber, ms_columnNumber  );
      } // if
      
      else if ( this.m_nextchar == '=' ) {
        PeekNextChar();
        return new Token( G.PE, "+=", ms_lineNumber, ms_columnNumber  );
      } // else if
      
      else
        return new Token( G.PLUS, "+", ms_lineNumber, ms_columnNumber  );
    } // else if
    
    else if ( first == '-' ) { // 符號
      if ( this.m_nextchar == '-' ) {
        PeekNextChar();
        return new Token( G.MM, "--", ms_lineNumber, ms_columnNumber  );
      } // if
      
      else if ( this.m_nextchar == '=' ) {
        PeekNextChar();
        return new Token( G.ME, "-=", ms_lineNumber, ms_columnNumber  );
      } // else if
      
      else
        return new Token( G.MINUS, "-", ms_lineNumber, ms_columnNumber  );
    } // else if
  
    else if ( first == '*' ) { // 符號
      if ( this.m_nextchar == '=' ) {
        PeekNextChar();
        return new Token( G.TE, "*=", ms_lineNumber, ms_columnNumber  );
      } // if
      
      else
        return new Token( G.STAR, "*", ms_lineNumber, ms_columnNumber  );
    } // else if
    
    else if ( first == '/' ) {  // 單個通常是註解
      if ( this.m_nextchar == '/' ) {
        while ( !G.sin.AtEOLN()  ) {
          PeekNextChar();
          if ( m_nextchar == '\0' ) // 註解到結束eof
            return new Token( G.EOF, "", ms_lineNumber, ms_columnNumber  );
        } // while
        
        m_nextchar = GetNextNonWhiteSpaceChar();
        return FetchToken(); // 註解就找下個去
      } // if
      
      else if ( this.m_nextchar == '=' ) {
        PeekNextChar();
        return new Token( G.DE, "/=", ms_lineNumber, ms_columnNumber  );
      } // else if
      
      else
        return new Token( G.DIV, "/", ms_lineNumber, ms_columnNumber );
    } // else if
  
    else if ( first == '%' ) { // 符號
      if ( this.m_nextchar == '=' ) {
        PeekNextChar();
        return new Token( G.RE, "%=", ms_lineNumber, ms_columnNumber  );
      } // if
      
      else
        return new Token( G.PERCENT, "%", ms_lineNumber, ms_columnNumber  );
    } // else if
    
    else if ( first == '^' )  // ^
      return new Token( G.HAT, "^", ms_lineNumber, ms_columnNumber  );
    else if ( first == '(' )
      return new Token( G.LSP, "(", ms_lineNumber, ms_columnNumber  );
    else if ( first == ')'  ) 
      return new Token( G.RSP, ")", ms_lineNumber, ms_columnNumber  );
    else if ( first == '[' )
      return new Token( G.LMP, "[", ms_lineNumber, ms_columnNumber  );
    else if ( first == ']'  ) 
      return new Token( G.RMP, "]", ms_lineNumber, ms_columnNumber  );
    else if ( first == '{' )
      return new Token( G.LBP, "{", ms_lineNumber, ms_columnNumber  );
    else if ( first == '}'  ) 
      return new Token( G.RBP, "}", ms_lineNumber, ms_columnNumber  );
    else if ( first == ';' )
      return new Token( G.SC, ";", ms_lineNumber, ms_columnNumber  );
    else if ( first == ',' )
      return new Token( G.CM, ",", ms_lineNumber, ms_columnNumber  );
    else if ( first == '?' )
      return new Token( G.QM, "?", ms_lineNumber, ms_columnNumber  );
    else if ( IsBo( first ) ) {
      if ( first == ':' ) 
        return new Token( G.CL, ":", ms_lineNumber, ms_columnNumber  );
      else if ( first == '<' ) { // <= 或 <> 或<
        if ( m_nextchar == '=' ) {
          PeekNextChar();
          return new Token( G.LE, "<=", ms_lineNumber, ms_columnNumber  );
        } // if
        
        else if ( m_nextchar == '<' ) {
          PeekNextChar();
          return new Token( G.LS, "<<", ms_lineNumber, ms_columnNumber  );  
        } // else if
        
        else
          return new Token( G.LT, "<", ms_lineNumber, ms_columnNumber  );
      } // else if
      
      else if ( first == '>' ) { // >= 或 > 
        if ( m_nextchar == '=' ) { 
          PeekNextChar();
          return new Token( G.GE, ">=", ms_lineNumber, ms_columnNumber  );
        } // if
        
        else if ( m_nextchar == '>' ) {
          PeekNextChar();
          return new Token( G.RS, ">>", ms_lineNumber, ms_columnNumber  );  
        } // else if
        
        else 
          return new Token( G.GT, ">", ms_lineNumber, ms_columnNumber  );
      } // else if
      
      else if ( first == '=' ) { //
        if ( m_nextchar == '=' ) {
          PeekNextChar();
          return new Token( G.EQ, "==", ms_lineNumber, ms_columnNumber );  
        } // if
        
        else
          return new Token( G.HALF_EQ, "=", ms_lineNumber, ms_columnNumber  );  
      } // else if
      
      else if ( first == '!' ) { //
        if ( m_nextchar == '=' ) {
          PeekNextChar();
          return new Token( G.NEQ, "!=", ms_lineNumber, ms_columnNumber );  
        } // if
        
        else
          return new Token( G.HALF_NEQ, "!", ms_lineNumber, ms_columnNumber  );            
      } // else if 
      
      else if ( first == '&' ) { //
        if ( m_nextchar == '&' ) {
          PeekNextChar();
          return new Token( G.AND, "&&", ms_lineNumber, ms_columnNumber );  
        } // if
        
        else
          return new Token( G.HALF_AND, "&", ms_lineNumber, ms_columnNumber  );            
      } // else if 
      
      else if ( first == '|' ) { //
        if ( m_nextchar == '|' ) {
          PeekNextChar();
          return new Token( G.OR, "||", ms_lineNumber, ms_columnNumber );  
        } // if
        
        else
          return new Token( G.HALF_OR, "|", ms_lineNumber, ms_columnNumber  );            
      } // else if 
    } // else if 
    
    else if ( first == '\"' ) {  // 這邊可能會有錯***
      while ( m_nextchar != '\"' ) { 
        first = m_nextchar; 
        str = str + first;
        PeekNextChar();
      } // while
      
      PeekNextChar();
      str = str + first;
      return new Token( G.CONSTANT, str, ms_lineNumber, ms_columnNumber  );    
    } // else if
   
    else if ( first == '\'' ) { // 這裡需要再看看
      if ( m_nextchar == '\n' )
        return new Token( G.UNKNOWN, str, ms_lineNumber, ms_columnNumber  ); 
      PeekNextChar();
      str = str + first;
      if ( m_nextchar != '\'' )
        return new Token( G.UNKNOWN, str, ms_lineNumber, ms_columnNumber  ); 
      PeekNextChar();
      str = str + first;
      return new Token( G.CONSTANT, str, ms_lineNumber, ms_columnNumber  );    
    } // else if
    
    else   
      return new Token( G.UNKNOWN, str, ms_lineNumber, ms_columnNumber  );
    Token t = new Token();
    return t;
  } // FetchToken()
  
  public void PeekNextChar() throws Throwable {
    CharObj cx = new CharObj( '\0' );
    if ( G.sin.ReadChar( cx ) == false   ) {  // EOF
      m_nextchar = '\0';
      return;
    } // if
    
    m_nextchar = cx.val;
    if ( m_nextchar == '\n' ) {
      ms_lineNumber++;
      ms_columnNumber = 1;
    } // if
    else
      ms_columnNumber++;
  } // PeekNextChar()
  
  public char GetNextNonWhiteSpaceChar() throws Throwable {
    CharObj cx = new CharObj( '\0' );
    while ( cx.val == '\0' || cx.val == '\t' || cx.val == ' ' ||  cx.val == '\n' ) {
      if ( G.sin.ReadChar( cx ) == false   ) {  // EOF
        return '\0';
      } // if
      
      if ( cx.val == '\n' ) {
        ms_lineNumber++;
        ms_columnNumber = 1;
      } // if
      
      else
        ms_columnNumber++;
    } // while       
    
    return cx.val;
  } // GetNextNonWhiteSpaceChar()
  
  public boolean IsLetter( char c ) throws Throwable {
    if ( ( c >= 'a' && c <= 'z' ) || (  c >= 'A' &&  c <= 'Z' )  )
      return true;
    else
      return false;
  } // IsLetter()
  
  public boolean IsNum( char c ) throws Throwable {
    if ( c >= '0' && c <= '9' )
      return true;
    else
      return false;
  } // IsNum()  
  
  public boolean IsSign( char c ) throws Throwable {
    if ( c == '+' || c == '-' )
      return true;
    else 
      return false;
  } // IsSign()
  
  public boolean IsSpace( char c ) throws Throwable {
    if ( c == '\t' || c == ' ' || c == '\n' || c == '\0'  )
      return true;
    else
      return false;
  } // IsSpace()
  
  public boolean IsBo( char c ) throws Throwable {
    if ( c == '>' || c == '<' ||  c == '=' || c == ':' || c == '!' || c == '&' || c == '|'  )
      return true;
    else
      return false;
  } // IsBo()
  
  public ArrayList<Token> GetTokenList() throws Throwable {
    return mTokenlist;
  } // GetTokenList()
   
  public void EncounterError() throws Throwable {
    if ( m_nextchar == '\n' )
      return;
    while ( !G.sin.AtEOLN()  ) {
      PeekNextChar();
      if ( m_nextchar == '\0' ) // eof
        return;
    } // while
    
    PeekNextChar();
  } // EncounterError()
  
  public Token PeekToken() throws Throwable {
    mnow_token = FetchToken();
    return mnow_token;
  } // PeekToken() 
  
  
} // class SCANNER

class PARSER {
  public ArrayList<Token> mTokenList = null ;
  public ArrayList<Token> mtempList = null;
  public SCANNER msc = null; // myscanner
  public int mTCt; // 主要的計數器(index)
  public int mTCt_temp; // 
  public int m_nowCommand; // 現在在command的第幾個
  public boolean mError1 = false; // 字元錯誤
  public boolean mError2 = false; // 語法錯誤
  public boolean mError3 = false; // 未定義錯誤
  public boolean mExecute = false; // 讀到分號或是quit的處理
  public PARSER( SCANNER sc ) {
    mTokenList = new ArrayList<Token>();
    this.msc = sc;
    mTCt = 0; // token計數器
    m_nowCommand = 0;

  } // PARSER()
  
  public void FetchToken() throws Throwable {
    if ( mTokenList.size() == 0 ||  mTCt == mTokenList.size() ) {// token不夠需抓
      mTokenList.add( msc.FetchToken() );    
    } // if
    
    if ( mTCt == mTokenList.size()- 1 ) {// token不夠需抓
      mTokenList.add( msc.FetchToken() );
      mTCt++;
    } // if
    
    else if ( mTCt < mTokenList.size() ) {  // 有token就把count往前挪，不抓
      mTCt++;
    } // else if
  } // FetchToken()
  
  
  public void ParserIt()  throws Throwable {
    if ( mTokenList.size() == 0 )
      FetchToken();
    
    if ( GoUser_Input() == true ) {
      for ( Token a : mTokenList  ) {
        System.out.println( a.mvalue );
      } // for
      
      mTokenList.clear();
      mTCt = 0;
    } // if
    
    ErrorDetect();  
  } // ParserIt()
  
  public boolean Index_moving() throws Throwable {
    mTCt = mTCt_temp;
    if ( ErrorDetect() )
      return false;
    else
      return true;
  } // Input_Go()
  
  public boolean Save_index() throws Throwable { 
    mTCt_temp = mTCt;
    if ( ErrorDetect() )
      return false;
    else
      return true;  
  } // Save_index()
  
  public boolean GoUser_Input() throws Throwable {
    if ( IsType_Specifier() == true || mTokenList.get( mTCt ).mtype == G.VOID ) {
      if ( GoDefinition() == true ) { // 上面的條件是Go Definition
        return true;
      } // if
      
      else 
        return false;
    } // if 
    
    else if ( IsStatement() == true  ) { // 下一回合在看看
      if ( GoStatement() == true ) { // 上面的條件是Go Definition
        return true;
      } // if
      
      else 
        return false;
    } // else if
    
    else {
      mError2 = true;
      return false;
    } // else
  } // GoUser_Input()
  
    
  public boolean GoDefinition() throws Throwable {
    if ( IsType_Specifier() == true ) {
      GoType_Specifier();
      if ( mTokenList.get( mTCt ).mtype == G.IDENT ) {
        FetchToken();
        if ( GoFunction_Definition_Or_Declarators() == true )
          return true;
        else
          return false;
      } // if
      
      else {  // 不是ident
        mError2 = true;
        return false;
      } // else
    } // if
    
    else if ( mTokenList.get( mTCt ).mtype == G.VOID ) {
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype == G.IDENT ) {
        FetchToken();
        if ( GoFunction_Definition_Without_ID() == true )
          return true;
        else
          return false;
      } // if
      
      else {  // 不是ident
        mError2 = true;
        return false;
      } // else
    } // else if
    
    else { // error
      mError2 = true;
      return false;
    } // else
  } // GoDefinition()
  
  public boolean GoType_Specifier() throws Throwable { // 這個加
    if ( IsType_Specifier() == true ) {
        FetchToken();
      return true;  
    } // if
    else { 
      mError2 = true;  
      return false;
    } // else
  } // GoType_Specifier()
  
  public boolean GoFunction_Definition_Or_Declarators() throws Throwable { // 
    if ( mTokenList.get( mTCt ).mtype == G.LSP ) { // 小左括號就是GoFWithID
      if ( GoFunction_Definition_Without_ID() == true )
        return true;
      else
        return false;
    } // if
    
    else if ( mTokenList.get( mTCt ).mtype == G.LMP || mTokenList.get( mTCt ).mtype == G.SC || 
        mTokenList.get( mTCt ).mtype == G.CM ) {
      if ( GoRest_Of_Declarators() == true ) // 中左刮或逗號或分號就是GoFWithID
        return true;
      else
        return false;
    } // else if
    
    else { // error
      mError2 = true;
      return false;
    } // else
  } // GoFuncion_Definition_Or_Declarators()
  
  public boolean GoRest_Of_Declarators() throws Throwable {
    if ( mTokenList.get( mTCt ).mtype == G.LMP ) {
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype != G.CONSTANT ) { // 是數字就對不是就是error
        mError2 = true;
        return false;
      } // if
        
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype != G.RMP ) { // 是數字就對不是就是error
        mError2 = true;
        return false;
      } // if
          
      FetchToken();
    } // if  
     
    while ( mTokenList.get( mTCt ).mtype == G.CM  ) { // 可有可無
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype != G.IDENT  ) { // 是數字就對不是就是error
        mError2 = true;
        return false;
      } // if 
      
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype == G.LMP ) {
        FetchToken();
        if ( mTokenList.get( mTCt ).mtype != G.CONSTANT ) { // 是數字就對不是就是error
          mError2 = true;
          return false;
        } // if
          
        FetchToken();
        if ( mTokenList.get( mTCt ).mtype != G.RMP ) { // 是數字就對不是就是error
          mError2 = true;
          return false;
        } // if
            
        FetchToken();
      } // if
    } // while
    
    if (  mTokenList.get( mTCt ).mtype == G.SC  ) {
      FetchToken();
      return true;  
    } // else if

    else { // error
      mError2 = true;
      return false;
    } // else
  } // GoRest_Of_Declarators()
  
  public boolean GoFunction_Definition_Without_ID() throws Throwable {
    
    if ( mTokenList.get( mTCt ).mtype == G.LSP )  // 先左刮
      FetchToken();     
    else { // error
      mError2 = true;
      return false;
    } // else
    
    if ( mTokenList.get( mTCt ).mtype == G.VOID  ) { 
      FetchToken();
    } // if
    
    else if ( IsType_Specifier() == true ) { // formal_parameter_list開頭是type_specifer
      if ( GoFormal_Parameter_List() == false ) // 這樣if應該還是會跑
        return false;
    } // else if
    
    if ( mTokenList.get( mTCt ).mtype == G.RSP )  // 先左刮
      FetchToken();      
    else { // error
      mError2 = true;
      return false;
    } // else
     
    if ( GoCompound_Statement() == true )
      return true;
    else
      return false;
  } // GoFuction_Definition_Without_ID()
  
  public boolean GoFormal_Parameter_List() throws Throwable {
    if ( GoType_Specifier() != true ) {
      mError2 = true;
      return false;
    } // if  
     
    if ( mTokenList.get( mTCt ).mtype == G.HALF_AND ) {
      FetchToken();
    } // if
      
    if ( mTokenList.get( mTCt ).mtype != G.IDENT ) {
      mError2 = true;
      return false;
    } // if
    
    FetchToken();
    if ( mTokenList.get( mTCt ).mtype == G.LMP ) {
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype != G.CONSTANT ) { // 是數字就對不是就是error
        mError2 = true;
        return false;
      } // if
        
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype != G.RMP ) { // 是數字就對不是就是error
        mError2 = true; 
        return false;
      } // if
          
      FetchToken();
    } // if  

    while ( mTokenList.get( mTCt ).mtype == G.CM  ) { // 這個while 感覺是塞上面的東西  
      FetchToken();
      if ( GoType_Specifier() != true ) {
        mError2 = true;
        return false;
      } // if  
      
      
      if ( mTokenList.get( mTCt ).mtype == G.HALF_AND ) {
        FetchToken(); 
      } // if
      
      if ( mTokenList.get( mTCt ).mtype != G.IDENT ) {
        mError2 = true;
        return false;
      } // if
      
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype == G.LMP ) {
        FetchToken();
        if ( mTokenList.get( mTCt ).mtype != G.CONSTANT ) { // 是數字就對不是就是error
          mError2 = true;
          return false;
        } // if
          
        FetchToken();
        if ( mTokenList.get( mTCt ).mtype != G.RMP ) { // 是數字就對不是就是error
          mError2 = true;
          return false;
        } // if
            
        FetchToken();
      } // if  
    } // while
    
    return true;
  } // GoFormal_Parameter_List()
  
  public boolean GoCompound_Statement() throws Throwable {
    
    if ( mTokenList.get( mTCt ).mtype != G.LBP ) {
      mError2 = true;
      return false;
    } // if
    
    FetchToken();
    while ( IsType_Specifier() || IsStatement() ) { // declaration是type開頭
      if ( IsType_Specifier() == true ) {
        if ( GoDeclaration() != true )
          return false;
      } // if
      
      else if ( IsStatement() == true ) {
        if ( GoStatement() != true )
          return false;
      } // else if
    } // while
    
    if ( mTokenList.get( mTCt ).mtype != G.RBP ) {
      mError2 = true;
      return false;   
    } // if
    
    else { // 最後一個是右大刮
      FetchToken();
      return true;
    } // else
  } // GoCompound_Statement()
  
  public boolean GoDeclaration() throws Throwable {
    if ( GoType_Specifier() == false ) {
      mError2 = true;
      return false;
    } // if
    
    
    if ( mTokenList.get( mTCt ).mtype != G.IDENT ) {
      mError2 = true;
      return false;
    } // if
    
    FetchToken();
    if ( mTokenList.get( mTCt ).mtype == G.LMP || mTokenList.get( mTCt ).mtype == G.SC || 
        mTokenList.get( mTCt ).mtype == G.CM ) {
      if ( GoRest_Of_Declarators() == true ) // 中左刮或逗號或分號就是GoFWithID
        return true;
      else
        return false;
    } // if
    
    else { // error
      mError2 = true;
      return false;
    } // else          
  } // GoDeclaration()
  
  public boolean GoStatement() throws Throwable {
    if (  mTokenList.get( mTCt ).mtype == G.SC ) {
      return true;
    } // if
    
    else if (  IsExpression() == true ) {
      if ( GoExpression()  != true ) { // 中左刮或逗號或分號就是GoFWithID
        mError2 = true;
        return false;
      } // if
      
      if (  mTokenList.get( mTCt ).mtype == G.SC ) {
        return true;
      } // if
    } // else if
    
    else if (  mTokenList.get( mTCt ).mtype == G.RETURN ) {
     FetchToken();
     if (  IsExpression() == true ) {
       if ( GoExpression() == false ) // 中左刮或逗號或分號就是GoFWithID
         return false;  
     } // if
     
     if (  mTokenList.get( mTCt ).mtype == G.SC ) {
       return true;
     } // if
     
     else {
       mError2 = true;
       return false;  
     } // else
     
    } // else if
    
    else if (  mTokenList.get( mTCt ).mtype == G.LBP ) {
      if ( GoCompound_Statement() == true )
        return true;
      else
        return false;
    } // else if
    
    else if (  mTokenList.get( mTCt ).mtype == G.IF ) {
      FetchToken();
      if (  mTokenList.get( mTCt ).mtype != G.LSP ) {
        mError2 = true;
        return false;
      } // if
      
      FetchToken();
      if (  IsExpression() == false ) {
        mError2 = true;
        return false;
      } // if
      
      if ( GoExpression() == false )
        return false;
      
      if (  mTokenList.get( mTCt ).mtype != G.RSP ) {
        mError2 = true;
        return false;
      } // if
      FetchToken();
      
      if ( IsStatement() == false ) { // ****這邊可能有錯誤
        mError2 = true;
        return false;
      } // if
      
      if ( GoStatement() == false )
        return false;

      if ( mTokenList.get( mTCt ).mtype == G.ELSE ) {
        FetchToken();
        if ( IsStatement() == false ) { // ****這邊可能有錯誤
          mError2 = true;
          return false;
        } // if
        
        if ( GoStatement() == false )
          return false;
      } // if
      
      return true;
    } // else if
    
    else if (  mTokenList.get( mTCt ).mtype == G.WHILE ) {
      FetchToken();
      if (  mTokenList.get( mTCt ).mtype != G.LSP ) {
        mError2 = true;
        return false;
      } // if
      
      FetchToken();
      if (  IsExpression() == false ) {
        mError2 = true;
        return false;
      } // if
      
      if ( GoExpression() == false )
        return false;

      
      if (  mTokenList.get( mTCt ).mtype != G.RSP ) {
        return false;
      } // if     
      
      FetchToken();
      
      if ( IsStatement() == false ) { // ****這邊可能有錯誤
        mError2 = true;  
        return false;
      } // if
      
      if ( GoStatement() == false )
        return false;
      else
        return true;
    } // else if
    
    else if (  mTokenList.get( mTCt ).mtype == G.DO ) {
      FetchToken();
      if (  IsStatement() == false ) {
        mError2 = true;
        return false;
      } // if  
      
      if ( GoStatement() == false )
        return false;
      
      
      if ( mTokenList.get( mTCt ).mtype != G.WHILE ) { // ****這邊可能有錯誤
        mError2 = true;
        return false;
      } // if  下面是while
             
      FetchToken();
      if (  mTokenList.get( mTCt ).mtype != G.LSP ) {
        mError2 = true;
        return false;
      } // if
      
      FetchToken();
      if (  IsExpression() == false ) {
        mError2 = true;
        return false;
      } // if
      
      if ( GoExpression() == false )
        return false;
      
      if (  mTokenList.get( mTCt ).mtype != G.RSP ) {
        mError2 = true;        
        return false;
      } // if     
      
      FetchToken();
      if ( mTokenList.get( mTCt ).mtype != G.SC ) { // ****這邊可能有錯誤
        mError2 = true;
        return false;
      } // if
      
      else {
        return true; //最後是sc所以正確
      } // else
    } // else if  
    
    else {
      mError2 = true;  
      return false;  
    } // else 
    return true;
  } // GoStatement()
  
  public boolean GoExpression() throws Throwable {
    if ( mTCt >= mTokenList.size() )
      return false;
    if (  IsExpression() != true ) {
      mTCt++;
      return false;
    } // if
    
    if ( GoBasic_Expression() == false )
      return false;
    if ( mTCt >= mTokenList.size() )
      return false;
    
    while ( mTokenList.get( mTCt ).mtype == G.CM ) {
      mTCt++;
      if ( mTCt >= mTokenList.size() )
        return false;
      if (  IsExpression() != true ) {
        mTCt++;
        return false;
      } // if
  
      if ( GoBasic_Expression() == false )
        return false;
      if ( mTCt >= mTokenList.size() )
        return false;
    } // while
    
    return true;
  } // GoExpression()
  
  public boolean GoBasic_Expression() throws Throwable {
    FetchToken();
    return true;
  } // GoBasic_Expression()
  
 
  
  public boolean IsSign() throws Throwable {
    if ( mTokenList.get( mTCt ).mtype == G.PLUS || mTokenList.get( mTCt ).mtype == G.MINUS ||
        mTokenList.get( mTCt ).mtype == G.HALF_NEQ )
      return true;
    else 
      return false;
    
  } // IsSign() 
  
  public boolean IsStatement() throws Throwable { // 看statement的前綴字
    if ( mTokenList.get( mTCt ).mtype == G.SC     || IsExpression() ||
         mTokenList.get( mTCt ).mtype == G.RETURN || IsCompound_Statement()  || 
         mTokenList.get( mTCt ).mtype == G.IF  ||  mTokenList.get( mTCt ).mtype == G.WHILE  ||  
         mTokenList.get( mTCt ).mtype == G.DO )
      return true;
    else 
      return false;
  } // IsStatement() 
  
  public boolean IsCompound_Statement() throws Throwable { // expression就是basic_expression
    if ( mTokenList.get( mTCt ).mtype == G.LBP )
      return true;
    else 
      return false;
  } // IsStatement() 
  
  public boolean IsExpression() throws Throwable { // expression就是basic_expression
    if ( mTokenList.get( mTCt ).mtype == G.IDENT    || mTokenList.get( mTCt ).mtype == G.PP ||
         mTokenList.get( mTCt ).mtype == G.MM   ||  mTokenList.get( mTCt ).mtype == G.CONSTANT  || 
         mTokenList.get( mTCt ).mtype == G.LSP || IsSign() )
      return true;
    else 
      return false;
  } // IsStatement() 
  
  
  public boolean IsType_Specifier() throws Throwable {
    if ( mTokenList.get( mTCt ).mtype == G.INT || mTokenList.get( mTCt ).mtype == G.CHAR ||
        mTokenList.get( mTCt ).mtype == G.FLOAT || mTokenList.get( mTCt ).mtype == G.STRING  || 
        mTokenList.get( mTCt ).mtype == G.BOOL  )
      return true;
    else 
      return false;
  } // IsType_Specifier() 
  
  public boolean IsAssignment_Operator() throws Throwable {
    if ( mTokenList.get( mTCt ).mtype == G.HALF_EQ || mTokenList.get( mTCt ).mtype == G.TE ||
        mTokenList.get( mTCt ).mtype == G.DE       || mTokenList.get( mTCt ).mtype == G.RE  || 
        mTokenList.get( mTCt ).mtype == G.PE       || mTokenList.get( mTCt ).mtype == G.ME  )
      return true;
    else 
      return false;
  } // IsType_Specifier() 
  
  
  public void ClearIt() throws Throwable {
    mTCt = 0;
    m_nowCommand = 0;
    mTokenList.clear();  
    mError1 = false; // 字元錯誤
    mError2 = false; // 語法錯誤
    mError3 = false; // 未定義錯誤
    mExecute = false; // 讀到分號或是quit的處理

  } // ClearIt()
  
  
  public boolean ErrorDetect() throws Throwable {
    if ( mTokenList.size() <= 0 ) // 應該是不會有這種狀況
      return false;
    Token t = mTokenList.get( mTokenList.size() - 1 ); // 拿最後一項token = 最新讀的
    if ( t.mtype == G.UNKNOWN ) // 順便檢查Unrecognized
      mError1 = true;
    if ( mError1 || mError2 || mError3 )
      return true;
    else
      return false;
  } // ErrorDetect
  
  public void ErrorHandle() throws Throwable {
    if ( mTokenList.size() <= 0 ) // 應該是不會有這種狀況
      return;
    Token t = mTokenList.get( mTokenList.size() - 1 ); // 拿最後一項token = 最新讀的
    if ( t.mtype == G.UNKNOWN ) // 順便檢查Unrecognized
      mError1 = true;  
    if ( mError1 || mError2 ) {
      G.ErrorPrint( mError1, mError2, mError3, t  ) ;
      msc.EncounterError();  
      this.ClearIt();
    } // if
    
    else if ( mError3 ) { // undefine比較難處理
      Token f = null;
      int stoploop = 0;
      for ( int i = mTokenList.size() - 1 ; i >= 0 && stoploop == 0 ; i-- ) {
        f = mTokenList.get( i );
        if ( f.mtype == G.IDENT ) {
          if ( G.CheckIDInTable( f.mvalue ) == false )
            stoploop = 1;
        } // if
      } // for
      
      G.ErrorPrint( mError1, mError2, mError3, f  ) ;
      msc.EncounterError();  
      this.ClearIt();  
    } // else if 
  } // ErrorDetectAndHandle()
  
  
  public boolean GetExecuteState() {
    return mExecute;  
  } // GetExecuteState()
  
  public ArrayList<Token> GetTable() {
    return mTokenList;  
  } // GetTable()
} // class PARSER

class Evalutor {
 
} // class Evalutor







class Main {

  public static void main( String[] args ) throws Throwable {
    G.Init();
    SCANNER sc = new SCANNER();
    PARSER ps = new PARSER( sc );
    Evalutor eu = new Evalutor();
    G.s_utestnum = G.sin.ReadInt(); // 留著debug用
    G.sin.ReadChar(); // 讀掉換行
    G.CYPrint( "Program starts...\n" );
    while ( ! G.sin.AtEOF() && G.s_quit == 0 ) {
      ps.ParserIt();  
      
    } // while
    
    G.CYPrint( "> Program exits..." );
    return; 
  } // main()

} // class Main


