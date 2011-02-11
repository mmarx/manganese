// prevent double inclusion

#ifndef	MU32_DEFS_H
#define MU32_DEFS_H

#include <stdint.h>
#include <stdio.h>

#define REUSE(type) type
#define pascal
#define _export

#define STD_PRE std

#define mutT _T

#define mutChar char
#define mutString (char*)
#define mutStringRef mutString
#define mutEmptyString ((char *) NULL)
#define mutFreeString(string) if (string) free (string)
#define mutDelString(string) (mutFreeString(string), string = mutEmptyString)
#define mutFopen fopen
#define mutCopyString(left,right) left = strdup(right)
#define mutCopyIntoString(left,right) strcpy(left,right)
#define mutStrdup strdup
#define mutStrCmp(left,right) strcmp (left, right)
#define mutStrEq(left,right)  (!strcmp (left, right))
#define mutStrLast(x) (x[strlen(x)])
#define mutC_STR(x) (x)
#define _C_STR(x) (x)
#define C_STR(x) (x)


#define mutStrLen strlen
#define mutStrChr strchr
#define mutFileName

#define mutOFstream STD_PRE::ofstream
#define mutIFstream STD_PRE::ifstream
#define mutTextStrem STD_PRE::ifstream

#define mutOpenOFstream(name,filename) \
   STD_PRE::ofstream name(mutFileName(filename), STD_PRE::ios::out | STD_PRE::ios::binary/*0, filebuf::openprot*/)
#define mutOpenIFstream(name,filename) \
   STD_PRE::ifstream name(mutFileName(filename), STD_PRE::ios::in | STD_PRE::ios::binary/*0, filebuf::openprot*/)

#define mutWriteStream(stream,data,count) \
	stream.write(data,count)
#define mutReadStream(stream,data,count) \
	stream.read(data,count)
#define mutCloseStream(stream) stream.close()


#define mutPutC(stream,data) stream.putc(data)
#define mutGetC(stream) stream.getc()

#define mutStreamBad(stream) (stream.bad())
#define mutStreamGood(stream) (!stream.bad())
#define mutStreamEOF(stream) (stream.eof())

#define mutAssertMsg(cond,msg)

#define MIDI_MIN_CHANNEL 0
#define MIDI_MAX_CHANNEL 15
#define MIDI_MIN_KEY 0
#define MIDI_MAX_KEY 0x7f

typedef uint8_t BYTE;
typedef uint16_t DWORD;

typedef char wxChar;
typedef char mutTranslationChar;

#define _(x) x
#define _T(x) x

#endif /* MU32_DEFS_H */


