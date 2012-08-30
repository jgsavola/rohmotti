>>> Traceback (most recent call last):
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 20
    iv =
        ^
SyntaxError: invalid syntax
>>> session.encrypt
<function encrypt at 0x7f5221661140>
>>> session.encrypt('jee')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 13, in encrypt
    aes = AES.new('01234567', AES.MOD_CFB, iv)
AttributeError: 'module' object has no attribute 'MOD_CFB'
>>> help(AES)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'AES' is not defined
>>> 
>>> help(AES.)
  File "<stdin>", line 1
    help(AES.)
             ^
SyntaxError: invalid syntax
>>> AES.new
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'AES' is not defined
>>> from Crypto.Cipher import AES

>>> >>> 
>>> AES
<module 'Crypto.Cipher.AES' from '/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.pyc'>
>>> import session
>>> session.encrypt('jee')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 13, in encrypt
    aes = AES.new('01234567', AES.MOD_CFB, iv)
AttributeError: 'module' object has no attribute 'MOD_CFB'
>>> AES.new
<function new at 0x7f522165ce60>
>>> help(AES)
Help on module Crypto.Cipher.AES in Crypto.Cipher:

NAME
    Crypto.Cipher.AES - AES symmetric cipher

FILE
    /usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py

MODULE DOCS
    http://docs.python.org/library/Crypto.Cipher.AES

DESCRIPTION
    AES `(Advanced Encryption Standard)`__ is a symmetric block cipher standardized
    by NIST_ . It has a fixed data block size of 16 bytes.
    Its keys can be 128, 192, or 256 bits long.
    
    AES is very fast and secure, and it is the de facto standard for symmetric
    encryption.
    
    As an example, encryption can be done as follows:
    
        >>> from Crypto.Cipher import AES
        >>> from Crypto import Random
        >>>
        >>> key = b'Sixteen byte key'
        >>> iv = Random.new().read(AES.block_size)
        >>> cipher = AES.new(key, AES.MODE_CFB, iv)
        >>> msg = iv + cipher.encrypt(b'Attack at dawn')
    
    .. __: http://en.wikipedia.org/wiki/Advanced_Encryption_Standard
    .. _NIST: http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
    
    :undocumented: __revision__, __package__

CLASSES
    Crypto.Cipher.blockalgo.BlockAlgo
        AESCipher
    
    class AESCipher(Crypto.Cipher.blockalgo.BlockAlgo)
     |  AES cipher object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, key, *args, **kwargs)
     |      Initialize an AES cipher object
     |      
     |      See also `new()` at the module level.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Crypto.Cipher.blockalgo.BlockAlgo:
     |  
     |  decrypt(self, ciphertext)
     |      Decrypt data with the key and the parameters set at initialization.
     |      
     |      The cipher object is stateful; decryption of a long block
     |      of data can be broken up in two or more calls to `decrypt()`.
     |      That is, the statement:
     |          
     |          >>> c.decrypt(a) + c.decrypt(b)
     |      
     |      is always equivalent to:
     |      
     |           >>> c.decrypt(a+b)
     |      
     |      That also means that you cannot reuse an object for encrypting
     |      or decrypting other data with the same key.
     |      
     |      This function does not perform any padding.
     |      
     |       - For `MODE_ECB`, `MODE_CBC`, and `MODE_OFB`, *ciphertext* length
     |         (in bytes) must be a multiple of *block_size*.
     |      
     |       - For `MODE_CFB`, *ciphertext* length (in bytes) must be a multiple
     |         of *segment_size*/8.
     |      
     |       - For `MODE_CTR`, *ciphertext* can be of any length.
     |      
     |       - For `MODE_OPENPGP`, *plaintext* must be a multiple of *block_size*,
     |         unless it is the last chunk of the message.
     |      
     |      :Parameters:
     |        ciphertext : byte string
     |          The piece of data to decrypt.
     |      :Return: the decrypted data (byte string, as long as *ciphertext*).
     |  
     |  encrypt(self, plaintext)
     |      Encrypt data with the key and the parameters set at initialization.
     |      
     |      The cipher object is stateful; encryption of a long block
     |      of data can be broken up in two or more calls to `encrypt()`.
     |      That is, the statement:
     |          
     |          >>> c.encrypt(a) + c.encrypt(b)
     |      
     |      is always equivalent to:
     |      
     |           >>> c.encrypt(a+b)
     |      
     |      That also means that you cannot reuse an object for encrypting
     |      or decrypting other data with the same key.
     |      
     |      This function does not perform any padding.
     |      
     |       - For `MODE_ECB`, `MODE_CBC`, and `MODE_OFB`, *plaintext* length
     |         (in bytes) must be a multiple of *block_size*.
     |      
     |       - For `MODE_CFB`, *plaintext* length (in bytes) must be a multiple
     |         of *segment_size*/8.
     |      
     |       - For `MODE_CTR`, *plaintext* can be of any length.
     |      
     |       - For `MODE_OPENPGP`, *plaintext* must be a multiple of *block_size*,
     |         unless it is the last chunk of the message.
     |      
     |      :Parameters:
     |        plaintext : byte string
     |          The piece of data to encrypt.
     |      :Return:
     |          the encrypted data, as a byte string. It is as long as
     |          *plaintext* with one exception: when encrypting the first message
     |          chunk with `MODE_OPENPGP`, the encypted IV is prepended to the
     |          returned ciphertext.

FUNCTIONS
    new(key, *args, **kwargs)
        Create a new AES cipher
        
        :Parameters:
          key : byte string
            The secret key to use in the symmetric cipher.
            It must be 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes long.
        :Keywords:
          mode : a *MODE_** constant
            The chaining mode to use for encryption or decryption.
            Default is `MODE_ECB`.
          IV : byte string
            The initialization vector to use for encryption or decryption.
            
            It is ignored for `MODE_ECB` and `MODE_CTR`.
        
            For `MODE_OPENPGP`, IV must be `block_size` bytes long for encryption
            and `block_size` +2 bytes for decryption (in the latter case, it is
            actually the *encrypted* IV which was prefixed to the ciphertext).
            It is mandatory.
           
            For all other modes, it must be `block_size` bytes longs.
          counter : callable
            (*Only* `MODE_CTR`). A stateful function that returns the next
            *counter block*, which is a byte string of `block_size` bytes.
            For better performance, use `Crypto.Util.Counter`.
          segment_size : integer
            (*Only* `MODE_CFB`).The number of bits the plaintext and ciphertext
            are segmented in.
            It must be a multiple of 8. If 0 or not specified, it will be assumed to be 8.
        
        :Return: an `AESCipher` object

DATA
    MODE_CBC = 2
    MODE_CFB = 3
    MODE_CTR = 6
    MODE_ECB = 1
    MODE_OFB = 5
    MODE_OPENPGP = 7
    MODE_PGP = 4
    __revision__ = '$Id$'
    block_size = 16
    key_size = (16, 24, 32)


>>> session.encrypt('jee')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 13, in encrypt
    aes = AES.new('01234567', IV=iv)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 94, in new
    return AESCipher(key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 59, in __init__
    blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
    self._cipher = factory.new(key, *args, **kwargs)
ValueError: AES key must be either 16, 24, or 32 bytes long
>>> session.encrypt('jee')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 15, in encrypt
    ciphertext = aes.encrypt(plaintext)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 244, in encrypt
    return self._cipher.encrypt(plaintext)
ValueError: Input strings must be a multiple of 16 in length
>>> 'jee'.ljust(1)
'jee'
>>> 'jee'.ljust(33)
'jee                              '
>>> 'jee'.ljust(16)
'jee             '
>>> session.encrypt('jee')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 15, in encrypt
    plain_len = len(plaintext)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 244, in encrypt
    return self._cipher.encrypt(plaintext)
ValueError: Input strings must be a multiple of 16 in length
>>> import session
>>> session.encrypt('jee')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 15, in encrypt
    plain_len = len(plaintext)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 244, in encrypt
    return self._cipher.encrypt(plaintext)
ValueError: Input strings must be a multiple of 16 in length
>>> session.encrypt('jee')
'jee             '
"[\xc27f'\xf7\xa5\xfcf+{\x96\xa2\xfa1|f$nK\xa3\xc6\xdb)"
>>> session.encrypt('jee')
'jee             ' len 16
'hB\x92\xc9^\x0c*%f+{\x96\xa2\xfa1|f$nK\xa3\xc6\xdb)'
>>> ct = session.encrypt('jee')
'jee             ' len 16
>>> len(ct)
24
>>> substr(ct, 8)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'substr' is not defined
>>> help(ct)
no Python documentation found for '\x99\x15\xdad\x1f\x9f\xd8[f+{\x96\xa2\xfa1|f$nK\xa3\xc6\xdb)'

>>> help(str)
Help on class str in module __builtin__:

class str(basestring)
 |  str(object) -> string
 |  
 |  Return a nice string representation of the object.
 |  If the argument is a string, the return value is the same object.
 |  
 |  Method resolution order:
 |      str
 |      basestring
 |      object
 |  
 |  Methods defined here:
 |  
 |  __add__(...)
 |      x.__add__(y) <==> x+y
 |  
 |  __contains__(...)
 |      x.__contains__(y) <==> y in x
 |  
 |  __eq__(...)
 |      x.__eq__(y) <==> x==y
 |  
 |  __format__(...)
 |      S.__format__(format_spec) -> string
 |      
 |      Return a formatted version of S as described by format_spec.
 |  
 |  __ge__(...)
 |      x.__ge__(y) <==> x>=y
 |  
 |  __getattribute__(...)
 |      x.__getattribute__('name') <==> x.name
 |  
 |  __getitem__(...)
 |      x.__getitem__(y) <==> x[y]
 |  
 |  __getnewargs__(...)
 |  
 |  __getslice__(...)
 |      x.__getslice__(i, j) <==> x[i:j]
 |      
 |      Use of negative indices is not supported.
 |  
 |  __gt__(...)
 |      x.__gt__(y) <==> x>y
 |  
 |  __hash__(...)
 |      x.__hash__() <==> hash(x)
 |  
 |  __le__(...)
 |      x.__le__(y) <==> x<=y
 |  
 |  __len__(...)
 |      x.__len__() <==> len(x)
 |  
 |  __lt__(...)
 |      x.__lt__(y) <==> x<y
 |  
 |  __mod__(...)
 |      x.__mod__(y) <==> x%y
 |  
 |  __mul__(...)
 |      x.__mul__(n) <==> x*n
 |  
 |  __ne__(...)
 |      x.__ne__(y) <==> x!=y
 |  
 |  __repr__(...)
 |      x.__repr__() <==> repr(x)
 |  
 |  __rmod__(...)
 |      x.__rmod__(y) <==> y%x
 |  
 |  __rmul__(...)
 |      x.__rmul__(n) <==> n*x
 |  
 |  __sizeof__(...)
 |      S.__sizeof__() -> size of S in memory, in bytes
 |  
 |  __str__(...)
 |      x.__str__() <==> str(x)
 |  
 |  capitalize(...)
 |      S.capitalize() -> string
 |      
 |      Return a copy of the string S with only its first character
 |      capitalized.
 |  
 |  center(...)
 |      S.center(width[, fillchar]) -> string
 |      
 |      Return S centered in a string of length width. Padding is
 |      done using the specified fill character (default is a space)
 |  
 |  count(...)
 |      S.count(sub[, start[, end]]) -> int
 |      
 |      Return the number of non-overlapping occurrences of substring sub in
 |      string S[start:end].  Optional arguments start and end are interpreted
 |      as in slice notation.
 |  
 |  decode(...)
 |      S.decode([encoding[,errors]]) -> object
 |      
 |      Decodes S using the codec registered for encoding. encoding defaults
 |      to the default encoding. errors may be given to set a different error
 |      handling scheme. Default is 'strict' meaning that encoding errors raise
 |      a UnicodeDecodeError. Other possible values are 'ignore' and 'replace'
 |      as well as any other name registered with codecs.register_error that is
 |      able to handle UnicodeDecodeErrors.
 |  
 |  encode(...)
 |      S.encode([encoding[,errors]]) -> object
 |      
 |      Encodes S using the codec registered for encoding. encoding defaults
 |      to the default encoding. errors may be given to set a different error
 |      handling scheme. Default is 'strict' meaning that encoding errors raise
 |      a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and
 |      'xmlcharrefreplace' as well as any other name registered with
 |      codecs.register_error that is able to handle UnicodeEncodeErrors.
 |  
 |  endswith(...)
 |      S.endswith(suffix[, start[, end]]) -> bool
 |      
 |      Return True if S ends with the specified suffix, False otherwise.
 |      With optional start, test S beginning at that position.
 |      With optional end, stop comparing S at that position.
 |      suffix can also be a tuple of strings to try.
 |  
 |  expandtabs(...)
 |      S.expandtabs([tabsize]) -> string
 |      
 |      Return a copy of S where all tab characters are expanded using spaces.
 |      If tabsize is not given, a tab size of 8 characters is assumed.
 |  
 |  find(...)
 |      S.find(sub [,start [,end]]) -> int
 |      
 |      Return the lowest index in S where substring sub is found,
 |      such that sub is contained within S[start:end].  Optional
 |      arguments start and end are interpreted as in slice notation.
 |      
 |      Return -1 on failure.
 |  
 |  format(...)
 |      S.format(*args, **kwargs) -> string
 |      
 |      Return a formatted version of S, using substitutions from args and kwargs.
 |      The substitutions are identified by braces ('{' and '}').
 |  
 |  index(...)
 |      S.index(sub [,start [,end]]) -> int
 |      
 |      Like S.find() but raise ValueError when the substring is not found.
 |  
 |  isalnum(...)
 |      S.isalnum() -> bool
 |      
 |      Return True if all characters in S are alphanumeric
 |      and there is at least one character in S, False otherwise.
 |  
 |  isalpha(...)
 |      S.isalpha() -> bool
 |      
 |      Return True if all characters in S are alphabetic
 |      and there is at least one character in S, False otherwise.
 |  
 |  isdigit(...)
 |      S.isdigit() -> bool
 |      
 |      Return True if all characters in S are digits
 |      and there is at least one character in S, False otherwise.
 |  
 |  islower(...)
 |      S.islower() -> bool
 |      
 |      Return True if all cased characters in S are lowercase and there is
 |      at least one cased character in S, False otherwise.
 |  
 |  isspace(...)
 |      S.isspace() -> bool
 |      
 |      Return True if all characters in S are whitespace
 |      and there is at least one character in S, False otherwise.
 |  
 |  istitle(...)
 |      S.istitle() -> bool
 |      
 |      Return True if S is a titlecased string and there is at least one
 |      character in S, i.e. uppercase characters may only follow uncased
 |      characters and lowercase characters only cased ones. Return False
 |      otherwise.
 |  
 |  isupper(...)
 |      S.isupper() -> bool
 |      
 |      Return True if all cased characters in S are uppercase and there is
 |      at least one cased character in S, False otherwise.
 |  
 |  join(...)
 |      S.join(iterable) -> string
 |      
 |      Return a string which is the concatenation of the strings in the
 |      iterable.  The separator between elements is S.
 |  
 |  ljust(...)
 |      S.ljust(width[, fillchar]) -> string
 |      
 |      Return S left-justified in a string of length width. Padding is
 |      done using the specified fill character (default is a space).
 |  
 |  lower(...)
 |      S.lower() -> string
 |      
 |      Return a copy of the string S converted to lowercase.
 |  
 |  lstrip(...)
 |      S.lstrip([chars]) -> string or unicode
 |      
 |      Return a copy of the string S with leading whitespace removed.
 |      If chars is given and not None, remove characters in chars instead.
 |      If chars is unicode, S will be converted to unicode before stripping
 |  
 |  partition(...)
 |      S.partition(sep) -> (head, sep, tail)
 |      
 |      Search for the separator sep in S, and return the part before it,
 |      the separator itself, and the part after it.  If the separator is not
 |      found, return S and two empty strings.
 |  
 |  replace(...)
 |      S.replace(old, new[, count]) -> string
 |      
 |      Return a copy of string S with all occurrences of substring
 |      old replaced by new.  If the optional argument count is
 |      given, only the first count occurrences are replaced.
 |  
 |  rfind(...)
 |      S.rfind(sub [,start [,end]]) -> int
 |      
 |      Return the highest index in S where substring sub is found,
 |      such that sub is contained within S[start:end].  Optional
 |      arguments start and end are interpreted as in slice notation.
 |      
 |      Return -1 on failure.
 |  
 |  rindex(...)
 |      S.rindex(sub [,start [,end]]) -> int
 |      
 |      Like S.rfind() but raise ValueError when the substring is not found.
 |  
 |  rjust(...)
 |      S.rjust(width[, fillchar]) -> string
 |      
 |      Return S right-justified in a string of length width. Padding is
 |      done using the specified fill character (default is a space)
 |  
 |  rpartition(...)
 |      S.rpartition(sep) -> (head, sep, tail)
 |      
 |      Search for the separator sep in S, starting at the end of S, and return
 |      the part before it, the separator itself, and the part after it.  If the
 |      separator is not found, return two empty strings and S.
 |  
 |  rsplit(...)
 |      S.rsplit([sep [,maxsplit]]) -> list of strings
 |      
 |      Return a list of the words in the string S, using sep as the
 |      delimiter string, starting at the end of the string and working
 |      to the front.  If maxsplit is given, at most maxsplit splits are
 |      done. If sep is not specified or is None, any whitespace string
 |      is a separator.
 |  
 |  rstrip(...)
 |      S.rstrip([chars]) -> string or unicode
 |      
 |      Return a copy of the string S with trailing whitespace removed.
 |      If chars is given and not None, remove characters in chars instead.
 |      If chars is unicode, S will be converted to unicode before stripping
 |  
 |  split(...)
 |      S.split([sep [,maxsplit]]) -> list of strings
 |      
 |      Return a list of the words in the string S, using sep as the
 |      delimiter string.  If maxsplit is given, at most maxsplit
 |      splits are done. If sep is not specified or is None, any
 |      whitespace string is a separator and empty strings are removed
 |      from the result.
 |  
 |  splitlines(...)
 |      S.splitlines([keepends]) -> list of strings
 |      
 |      Return a list of the lines in S, breaking at line boundaries.
 |      Line breaks are not included in the resulting list unless keepends
 |      is given and true.
 |  
 |  startswith(...)
 |      S.startswith(prefix[, start[, end]]) -> bool
 |      
 |      Return True if S starts with the specified prefix, False otherwise.
 |      With optional start, test S beginning at that position.
 |      With optional end, stop comparing S at that position.
 |      prefix can also be a tuple of strings to try.
 |  
 |  strip(...)
 |      S.strip([chars]) -> string or unicode
 |      
 |      Return a copy of the string S with leading and trailing
 |      whitespace removed.
 |      If chars is given and not None, remove characters in chars instead.
 |      If chars is unicode, S will be converted to unicode before stripping
 |  
 |  swapcase(...)
 |      S.swapcase() -> string
 |      
 |      Return a copy of the string S with uppercase characters
 |      converted to lowercase and vice versa.
 |  
 |  title(...)
 |      S.title() -> string
 |      
 |      Return a titlecased version of S, i.e. words start with uppercase
 |      characters, all remaining cased characters have lowercase.
 |  
 |  translate(...)
 |      S.translate(table [,deletechars]) -> string
 |      
 |      Return a copy of the string S, where all characters occurring
 |      in the optional argument deletechars are removed, and the
 |      remaining characters have been mapped through the given
 |      translation table, which must be a string of length 256 or None.
 |      If the table argument is None, no translation is applied and
 |      the operation simply removes the characters in deletechars.
 |  
 |  upper(...)
 |      S.upper() -> string
 |      
 |      Return a copy of the string S converted to uppercase.
 |  
 |  zfill(...)
 |      S.zfill(width) -> string
 |      
 |      Pad a numeric string S with zeros on the left, to fill a field
 |      of the specified width.  The string S is never truncated.
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  __new__ = <built-in method __new__ of type object>
 |      T.__new__(S, ...) -> a new object with type S, a subtype of T

>>> ct[0:8]
'\x99\x15\xdad\x1f\x9f\xd8['
>>> len(ct[0:8])
8
>>> session.decrypt(ct)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 31, in decrypt
    plaintext = aes.decrypt(ciphertext)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 295, in decrypt
    return self._cipher.decrypt(ciphertext)
ValueError: Input strings must be a multiple of 16 in length
>>> session.decrypt(ct)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 31, in decrypt
    plaintext = aes.decrypt(ciphertext[8:end])
NameError: global name 'end' is not defined
>>> session.decrypt(ct)
'jee             '
>
>>> import base64
>>> base64.b64encode(ct)
'mRXaZB+f2FtmK3uWovoxfGYkbkujxtsp'
>>> b64ct base64.b64encode(ct)
  File "<stdin>", line 1
    b64ct base64.b64encode(ct)
               ^
SyntaxError: invalid syntax
>>> b64ct = base64.b64encode(ct)
>>> session.decrypt(base64.b64decode(b64ct))
'jee             '
>>> session.decrypt(base64.b64decode(b64ct))
'jee             '
>>> session.decrypt(base64.b64decode(b64ct))
'jee             '
>>> session.decrypt(base64.b64decode(b64ct))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 32, in decrypt
    aes = AES.new('0123456789abcdef', Mode=AES.MODE_CFB, IV=iv)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 94, in new
    return AESCipher(key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 59, in __init__
    blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
    self._cipher = factory.new(key, *args, **kwargs)
TypeError: 'Mode' is an invalid keyword argument for this function
>>> session.decrypt(base64.b64decode(b64ct))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 32, in decrypt
    aes = AES.new('0123456789abcdef', mode=AES.MODE_CFB, IV=iv)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 94, in new
    return AESCipher(key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 59, in __init__
    blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
    self._cipher = factory.new(key, *args, **kwargs)
TypeError: 'Mode' is an invalid keyword argument for this function
>>> session.decrypt(base64.b64decode(b64ct))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jonne/public_html/rohmotti/src/resepti/session.py", line 32, in decrypt
    aes = AES.new('0123456789abcdef', mode=AES.MODE_CFB, IV=iv)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 94, in new
    return AESCipher(key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 59, in __init__
    blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
    self._cipher = factory.new(key, *args, **kwargs)
ValueError: IV must be 16 bytes long
>>> session.decrypt(base64.b64decode(b64ct))
'\x1eNu+\xf8o\xd0\x84\x8f\xa5+s\xa2>\x89\x01'
>>> session.decrypt(session.encrypt('jee'))
'\xd2\xce\x8c0\xcc\x0f\xd2\xa1\xbfcm\xd5\xddM\x8a\xac        '
>>> session.decrypt(session.encrypt('jee'))
'5A\xce\x08\xeb>h6\xf9\xaa&\xadn\xb0\xc1\x10        '
>>> session.decrypt(session.encrypt('jee'))
'\xd6:[Y\xa7e7\x07\xf4Z\xc2C\xc1\t\xa4-        '
>>> session.decrypt(session.encrypt('jee'))
'a\xb2\x9f\xe9e\xaby\xa6o\x96\xc75\xe8B\xd3\t        '
>>> session.decrypt(session.encrypt('jee'))
'\x98!\xa7\xd0\xf0\x8em[\x88\x95\xdf\x8a|\xba\xe1\x9e        '
>>> session.decrypt(session.encrypt('jee'))
'K{\xd2\x0fg\x9d\xfcK\x94\xcad\xd9\x88vr\xba        '
>>> session.decrypt(session.encrypt('jee'))
'jee             '
>>> session.decrypt(session.encrypt('jee'))
'\x8a~7xp\xdf\xb0\xf4\xbbu\xaf\xfb\x8c\xd4#\xda'
>>> session.decrypt(session.encrypt('jee'))
'\xe6\xfe\x80\x8f\xed\xed\xc33`\x9c\x8a\x98V\xcdx\x18'
>>> session.decrypt(session.encrypt('jee'))
"-\x906'~t_\xacU9\xb4r\xe5\xf9E\xe9"
>>> session.decrypt(session.encrypt('jee'))
'\xbc\xa9\xf5(\\\x14\x88\x84Z\x14`_\xe4\\\x11\x1e'
>>> session.decrypt(session.encrypt('jee'))
'\xbf]\x0f\xc4\x1e!+\x96I\xd7\x11\xe4)\xe1`\x0b'
>>> session.decrypt(session.encrypt('jee'))
'\xc34\xdc\x00]e\x8c\xd8\x98\xb8\x1aa\xfc|\xcb\x05'
>>> session.decrypt(session.encrypt('jee'))
'\xab\xd4D\xe4{\xc9\x8ay\xdduqt\x86qm\x89'
>>> session.decrypt(session.encrypt('jee'))
'jee             '
>>> session.decrypt(session.encrypt('jee'))
'jee             '
>>> session.decrypt(session.encrypt('id=62 2012-08-30T21:29:30 xyzzy'))
'id=62 2012-08-30T21:29:30 xyzzy '
>>> session.encrypt('id=62 2012-08-30T21:29:30 xyzzy'
... 
... 
... )
'\xf9xP$\xc4\x80{y\x0c\xa0\x85d\xc2|z*\xd1\xb0N5\x97\xfb+Fu\\\x82\x04\xd5IJ\x12I\xf4\xa5\x04\xf2s\xe3<\xdb\xe1:\x9a_(\xaea'
>>> session.encrypt('id=62 2012-08-30T21:29:30 xyzzy')
'&\x1b\xdd\x9e3\xa0\xfc\x99\\\xc0\xa5\xe4z\x02\x1fXW\xfc\t\xb4\xfc\xcf\xbc\x1d\x84n\xe0<\x87\x93\xb8\xe0ZVrZ\xee\x13\x8c\x85\xe9`wv">3l'
>>> len(session.encrypt('id=62 2012-08-30T21:29:30 xyzzy'))
48
>>> base64.b64encode(len(session.encrypt('id=62 2012-08-30T21:29:30 xyzzy')))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/base64.py", line 53, in b64encode
    encoded = binascii.b2a_base64(s)[:-1]
TypeError: must be string or buffer, not int
>>> base64.b64encode(session.encrypt('id=62 2012-08-30T21:29:30 xyzzy'))
'3wHPyX9T4Q9txg7LhOGQhe/Vfq8ADX+SzKllSMF4is3iOQSRXiSF6HKrDRkyaFZx'
>>> base64.b64encode(session.encrypt('id=6233 2012-08-30T21:29:30 xyzzy'))
'VpcO2ivb161FAB9B2CZ5V+QKirsVGKQ83CqzqQAdMP+o3k4+uIax90xEevTPB7WXpKzbMY4qhh1pHesbBHhvvA=='
>>> base64.b64encode(session.encrypt('id=62 2012-08-30T21:29:30 xyzzy'))
'xyp1Un8FUWtOVY0IpAqcEsBvnwKSKUf8od+MEXGyFRz/F8tt56CSXRVXHtJ8b5UW'
>>> base64.b64encode(session.encrypt('id=621 2012-08-30T21:29:30 xyzzy'))
'LpuAaZwYANGjoybtQsy00fmIBO9H04EdD9nIOvSd5gB6KTOCNPrpg7kL2kZ6Nks1'
>>> 