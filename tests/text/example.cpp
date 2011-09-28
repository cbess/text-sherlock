/***************************************************************************
                    ansigenerator.cpp  -  description
                             -------------------
    begin                : Jul 5 2004
    copyright            : (C) 2004 by André Simon
    email                : andre.simon1@gmx.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#include "ansigenerator.h"

using namespace std;

namespace highlight {


string  AnsiGenerator::getOpenTag(const string&font,
                                  const string&fgCol, const string&bgCol) {
    ostringstream s;
    s  << "\033["<<font;
    if (!fgCol.empty())
        s<<";"<<fgCol;
    if (!bgCol.empty())
        s<<";"<<bgCol;
    s << "m";
    return  s.str();
}


AnsiGenerator::AnsiGenerator(const string &colourTheme)
        : CodeGenerator(colourTheme) {
    styleTagOpen.push_back("");
    styleTagOpen.push_back(getOpenTag("00", "31")); //str
    styleTagOpen.push_back(getOpenTag("00", "34"));//number
    styleTagOpen.push_back(getOpenTag("00", "34"));//sl comment
    styleTagOpen.push_back(getOpenTag("00", "34"));//ml comment
    styleTagOpen.push_back(getOpenTag("00", "35"));//escapeChar
    styleTagOpen.push_back(getOpenTag("00", "35"));//directive
    styleTagOpen.push_back(getOpenTag("01", "31"));//directive string
    styleTagOpen.push_back(getOpenTag("00", "30"));//linenum
    styleTagOpen.push_back(getOpenTag("01", "00"));//symbol

    styleTagClose.push_back("");
    for (int i=1;i<NUMBER_BUILTIN_STYLES; i++) {
        styleTagClose.push_back("\033[m");
    }
    newLineTag = "\n";
    spacer = " ";
}

AnsiGenerator::AnsiGenerator() {}
AnsiGenerator::~AnsiGenerator() {}

string AnsiGenerator::getHeader(const string & title) {
    return string();
}

void AnsiGenerator::printBody() {
    processRootState();
}

string AnsiGenerator::getFooter() {
    return string();
}

string AnsiGenerator::maskCharacter(unsigned char c) {
    string m;
    m+=c;
    return m;
}

string AnsiGenerator::getMatchingOpenTag(unsigned int styleID) {
    return (styleID)?getOpenTag("01", "32", ""):getOpenTag("00", "33");
}

string AnsiGenerator::getMatchingCloseTag(unsigned int styleID) {
    return "\033[m";
}

}
/***************************************************************************
                         ansicode.h  -  description
                             -------------------
    begin                : Jul 5 2004
    copyright            : (C) 2004 by Andre Simon
    email                : andre.simon1@gmx.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#ifndef ANSIGENERATOR_H
#define ANSIGENERATOR_H

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

#include "codegenerator.h"
#include "charcodes.h"
#include "version.h"

namespace highlight {

/**
   \brief This class generates ANSI escape sequences.

   It contains information about the resulting document structure (document
   header and footer), the colour system, white space handling and text
   formatting attributes.

* @author Andre Simon
*/

class AnsiGenerator : public highlight::CodeGenerator
  {
  public:

   /** Constructor
     \param colourTheme Name of Colour theme to use
    */
    AnsiGenerator( const string &colourTheme);
    AnsiGenerator();
    ~AnsiGenerator();

   /** prints document header
       \param  title Title of the document
    */
    string getHeader(const string & title);

    /** Prints document footer*/
    string getFooter();

    /** Prints document body*/
    void printBody();

  private:

    /** \return escaped character*/
    virtual string maskCharacter(unsigned char );


    /** gibt ANSI-"Tags" zurueck (Farbindex+bold+kursiv)*/
    string getOpenTag(const string&font,
                      const string&fgCol, const string&bgCol="");



    string getMatchingOpenTag(unsigned int styleID);
    string getMatchingCloseTag(unsigned int styleID);
  };

}
#endif
/*
 * Copyright (c) 1998,1999,2000,2001,2002 Tal Davidson. All rights reserved.
 *
 * ASBeautifier.cpp
 * by Tal Davidson (davidsont@bigfoot.com)
 * This file is a part of "Artistic Style" - an indentater and reformatter
 * of C, C, C# and Java source files.
 *
 * The "Artistic Style" project, including all files needed to compile it,
 * is free software; you can redistribute it and/or use it and/or modify it
 * under the terms of the GNU General Public License as published 
 * by the Free Software Foundation; either version 2 of the License, 
 * or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You should have received a copy of the GNU General Public
 * License along with this program.
 *
 * Patches:
 * 18 March 1999 - Brian Rampel -
 *       Fixed inverse insertion of spaces vs. tabs when in -t mode.
 * 08 may 2004 
 *       applied ASBeautifier.cpp.BITFIELD.patch.bz2
 */

#include "compiler_defines.h"
#include "ASBeautifier.h"

#include <vector>
#include <string>
#include <cctype>
#include <algorithm>
#include <iostream>


#define INIT_CONTAINER(container, value)     {if ( (container) != NULL ) delete (container); (container) = (value); }
#define DELETE_CONTAINER(container)          {if ( (container) != NULL ) delete (container) ; }

#ifdef USES_NAMESPACE
using namespace std;
#endif




#ifdef USES_NAMESPACE
namespace astyle
  {
#endif

  bool ASBeautifier::calledInitStatic = false;

  vector<const string*> ASBeautifier::headers;
  vector<const string*> ASBeautifier::nonParenHeaders;
  vector<const string*> ASBeautifier::preBlockStatements;
  vector<const string*> ASBeautifier::assignmentOperators;
  vector<const string*> ASBeautifier::nonAssignmentOperators;

  /*
   * initialize the static vars
   */
  void ASBeautifier::initStatic()
  {
    if (calledInitStatic)
      return;

    calledInitStatic = true;

    headers.push_back(&AS_IF);
    headers.push_back(&AS_ELSE);
    headers.push_back(&AS_FOR);
    headers.push_back(&AS_WHILE);
    headers.push_back(&AS_DO);
    headers.push_back(&AS_TRY);
    headers.push_back(&AS_CATCH);
    headers.push_back(&AS_FINALLY);
    headers.push_back(&AS_SYNCHRONIZED);
    headers.push_back(&AS_SWITCH);
    headers.push_back(&AS_CASE);
    headers.push_back(&AS_DEFAULT);
    headers.push_back(&AS_FOREACH);
    headers.push_back(&AS_LOCK);
    headers.push_back(&AS_UNSAFE);
    headers.push_back(&AS_FIXED);
    headers.push_back(&AS_GET);
    headers.push_back(&AS_SET);
    headers.push_back(&AS_ADD);
    headers.push_back(&AS_REMOVE);
    //headers.push_back(&AS_PUBLIC);
    //headers.push_back(&AS_PRIVATE);
    //headers.push_back(&AS_PROTECTED);

    //headers.push_back(&AS_OPERATOR);
    headers.push_back(&AS_TEMPLATE);
    headers.push_back(&AS_CONST);
    /**/
    headers.push_back(&AS_STATIC);
    headers.push_back(&AS_EXTERN);

    nonParenHeaders.push_back(&AS_ELSE);
    nonParenHeaders.push_back(&AS_DO);
    nonParenHeaders.push_back(&AS_TRY);
    nonParenHeaders.push_back(&AS_FINALLY);
    nonParenHeaders.push_back(&AS_STATIC);
    nonParenHeaders.push_back(&AS_CONST);
    nonParenHeaders.push_back(&AS_EXTERN);
    nonParenHeaders.push_back(&AS_CASE);
    nonParenHeaders.push_back(&AS_DEFAULT);
    nonParenHeaders.push_back(&AS_UNSAFE);
    nonParenHeaders.push_back(&AS_GET);
    nonParenHeaders.push_back(&AS_SET);
    nonParenHeaders.push_back(&AS_ADD);
    nonParenHeaders.push_back(&AS_REMOVE);



    nonParenHeaders.push_back(&AS_PUBLIC);
    nonParenHeaders.push_back(&AS_PRIVATE);
    nonParenHeaders.push_back(&AS_PROTECTED);
    nonParenHeaders.push_back(&AS_TEMPLATE);
    nonParenHeaders.push_back(&AS_CONST);
    ///    nonParenHeaders.push_back(&AS_ASM);

    preBlockStatements.push_back(&AS_CLASS);
    preBlockStatements.push_back(&AS_STRUCT);
    preBlockStatements.push_back(&AS_UNION);
    preBlockStatements.push_back(&AS_INTERFACE);
 