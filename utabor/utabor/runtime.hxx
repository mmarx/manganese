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

// ------------------------------------------------------------------
// Mutabor 2.win, 1997, R.Krauﬂe
// Laufzeitfunktionen der DLL
// ------------------------------------------------------------------

#if ! defined (__RUNTIME_H_INCLUDED)
#define __RUNTIME_H_INCLUDED

#include "defs.hxx"

#if !defined(__WXMSW__)
#ifndef UINT
#define UINT unsigned int
#endif
#define pascal
#endif
#include <setjmp.h>

typedef void UpdateUICallback();
typedef void KeyChangedCallback (int);
typedef void ParameterChangedCallback (int, int);

extern "C"
{
	extern bool RealTime;

	extern jmp_buf weiter_gehts_nach_compilerfehler;
	extern UpdateUICallback* updateUIcallback;
  extern KeyChangedCallback* key_changed_callback;
  extern ParameterChangedCallback* anchor_changed_callback;
  extern ParameterChangedCallback* width_changed_callback;

	char pascal Compile( void *compWin, const char *name );

  bool pascal
  Activate(bool realTime,
	   UpdateUICallback* callback,
	   KeyChangedCallback* key_change,
	   ParameterChangedCallback* anchor_change,
	   ParameterChangedCallback* width_change);
	void pascal Stop();
	void pascal Panic();

//  void pascal InDeviceActionAll(char action);

	bool pascal CheckNeedsRealTime();

	// box = -1 ... weiterlesen in angefangener Liste
	char pascal GetMutTag(char &isLogic, char *text, char *einsttext, char &key, int box = -1);
	char pascal IsLogicKey(char key);
	bool pascal KeyChanged(int box);
	bool pascal TSChanged(int box);
	bool pascal InDevicesChanged();
	void pascal GetDrivers(int *driver);
	void pascal SetDrivers(int *driver);
	char pascal GetChannels(char start, int &base, int &from, int &to, int &thru);
	void pascal SetChannels(int base, int from, int to, int thru);
	void pascal SetAktuellesKeyboardInstrument(int instr);
	int  pascal GetAktuellesKeyboardInstrument();


	void pascal GetTimerData(UINT &min, UINT &max);
}

#endif

