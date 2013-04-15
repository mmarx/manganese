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

// ##################################################################
// Mutabor 3, Header execute file
// ##################################################################

#ifndef EXECUTE_H
#define EXECUTE_H

#include "interpreter.hxx"

void KeyboardIn(int box, const mutChar *keys);

void GlobalReset();

void AddKey(int box, int taste, int id);

void DeleteKey(int box, int taste, int id);

void MidiAnalysis(int box, BYTE midiByte);

extern ton_system *tonsystem[MAX_BOX];

void protokoll_aktuelles_tonsystem( int instr );

void protokoll_liegende_frequenzen( int instr );

void protokoll_aktuelle_relationen( int instr );

void protokoll_liegende_relationen( int instr );

void FlushUpdateUI();

#define FLUSH_UPDATE_UI FlushUpdateUI()
#endif

