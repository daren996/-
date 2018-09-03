// CALD_to_Text.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#define MAX_CHAR 100000

int _tmain(int argc, _TCHAR* argv[])
{

	FILE *fpin, *fpout;

	char str[MAX_CHAR];
	char buffer[MAX_CHAR];
	char temp[MAX_CHAR];
	char *ptr, *ptrp;
	int lword, flagStr, i;

	fopen_s(&fpin, "CALD", "r");
	fopen_s(&fpout, "out.txt", "w");
	if( fpin == NULL || fpout == NULL)
	{
		printf("Error in opening file.\n");
		exit(0);
	}

	
	while( fgets( str, MAX_CHAR, fpin) != NULL)
	{
		if((int)(strchr(str, '\0') - str + 1) <= MAX_CHAR)
		{
			flagStr = 1;
		} else {
			flagStr = 0;
		}

		// word find
		ptr = strchr(str, '\t');
		lword = (int)(ptr - str);
		strncpy_s( buffer, str, lword);
		buffer[lword] = '\0';
		fprintf_s(fpout, "\n%s\t", buffer);
		printf("\n%s", buffer);
		
		// verb or noun or adverb find
		ptr = strstr( str, "<font color=orange>");
		if( ptr != NULL)
		{
			labelv:ptr = ptr + strlen("<font color=orange>");

			i = (int)( strstr( ptr, "</font>") - ptr);
			strncpy_s( buffer, ptr, i);
			buffer[i] = '\0';
			fprintf_s(fpout, "%s ", buffer);
			ptr = strstr( ptr, "<font color=orange>");
			if( ptr != NULL)
			{
				goto labelv;
			} else
				fprintf_s(fpout, "\t", buffer);
		} else
			fprintf_s(fpout, " \t", buffer);
		// definition find

		do
		{
			if((int)(strchr(str, '\0') - str + 1) <= MAX_CHAR)
				flagStr = 1;
			else
				flagStr = 0;

			ptrp = str;
			label:ptr = strstr( ptrp, "padding-left:5pt;");
			if( ptr == NULL && flagStr == 1)
				break;
			else if( ptr == NULL && flagStr == 0)
			{
				strncpy_s( buffer, str + 900, 100);
				strncpy_s( str, buffer, 100);
				fgets( str+100, MAX_CHAR, fpin);
				
			} else{
				ptr = strstr( ptr, "<div class=\"stylediv\">");
				i = (int)(strstr( ptr, "</div>") - ptr );
				strncpy_s( buffer, ptr, i);
				buffer[i] = '\0';
				ptrp = ptr;
				ptr = buffer;
				while(ptr != NULL)
				{
					ptr = strchr( ptr, '>');
					i = strchr( ptr, '<') == NULL? (int)(strchr( ptr, '\0') - ptr) : (int)(strchr( ptr, '<') - ptr);
					strncpy_s( temp, ptr + 1, i-1);
					temp[i-1] = '\0';
					fprintf_s(fpout, "%s", temp);
					ptr = ptr + i;
					if( *ptr == '\0')
						break;
				}
				fprintf_s(fpout, "\t");
				
				goto label;
			}

		}while(flagStr == 0);
	}

	fclose( fpin);
	fclose( fpout);
	return 0;
}

