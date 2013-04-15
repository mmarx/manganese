/***********************************************************************
 * manganese - midi analysis & visualization platform
 * Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301 USA.
 **********************************************************************/

#ifndef MU32_HILFS_H
#define MU32_HILFS_H

#include <cstdio>

#define HEAP_PORTION_SYNTAX   /*65536L*/ 64000
#define HEAP_PORTION_LAUFZEIT /*65536L*/ 64000

int  intern_fgetc( FILE *stream );
int  intern_ungetc( int c, FILE *stream );

void xfree (void * pointer);
void * xmalloc (size_t size);
void * xrealloc (void * block, size_t newsize);
void * xcalloc (size_t anzahl, size_t size);

void yfree (void * pointer);
void * ymalloc (size_t size);
void * yrealloc (void * block, size_t newsize);
void * ycalloc (size_t anzahl, size_t size);

int loesche_syntax_speicher ( void );
int init_syntax_speicher ( void );
int init_laufzeit_speicher ( void );
int loesche_laufzeit_speicher ( void );
void * xalloca (size_t size);
void xde_alloca (void * pointer);

#endif /* MU32_HILFS_H */


