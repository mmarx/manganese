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

/** \file
 ********************************************************************
 * Mutabor runtime functions.
 *
 * $Header: /cvsroot/mutabor/mutabor/mu32/Runtime.cpp,v 1.15 2010-11-21 13:15:45 keinstein Exp $
 * Copyright:   (c) 1997-2007 TU Dresden
 * \author R√ºdiger Krau√üe <krausze@mail.berlios.de>
 * Tobias Schlemmer <keinstein@users.berlios.de>
 * \date $Date: 2010-11-21 13:15:45 $
 * \version $Revision: 1.15 $
 * \license wxWindows license
 *
 * $Log: Runtime.cpp,v $
 * Revision 1.15  2010-11-21 13:15:45  keinstein
 * merged experimental_tobias
 *
 * Revision 1.14.2.9  2010-11-20 21:58:16  keinstein
 * reactivate midi playback
 *
 * Revision 1.14.2.8  2010-11-14 22:29:53  keinstein
 * Remvoed EDevice.cpp and EDevice.h from the sources list
 * They still reside in the source tree, since they have been used for Midi/GMN
 * file playing. That funcitonality has been disabled so far.
 * After reimplementation the files can be removed.
 *
 * Revision 1.14.2.7  2010-05-07 11:40:27  keinstein
 * actual_settings
 *
 * Revision 1.14.2.6  2010/04/15 09:28:43  keinstein
 * changing routes works, but is not honoured by MIDI, yet
 *
 * Revision 1.14.2.5  2010/03/30 08:38:27  keinstein
 * added rudimentary command line support
 * changed debug system to allow selection of messages via command line
 * further enhancements to the route dialogs
 *
 * Revision 1.14.2.4  2010/01/14 09:34:24  keinstein
 * Checkin searching for a bug
 *
 * Revision 1.14.2.3  2009/11/03 12:39:31  keinstein
 * input device dialog: Allow to edit input devices
 * fix a bug on Mac OS X, that prevented Mutabor from starting if no MIDI device is availlable
 *
 * Revision 1.14.2.2  2009/08/10 11:15:46  keinstein
 * some steps towards new route window
 *
 * Revision 1.14.2.1  2009/08/04 11:30:49  keinstein
 * removed mut.h
 *
 * Revision 1.14  2008/10/27 14:57:51  keinstein
 * Moved CurrentTimer stuff to Device
 *
 * Revision 1.13  2008/10/19 23:08:32  krausze
 * Dateien und Anpassungen f¸r Microsoft Visual Studio 8 (VC8)
 *
 * Revision 1.12  2008/10/10 08:33:19  keinstein
 * make compile on windws
 *
 * Revision 1.11  2008/10/01 09:31:07  keinstein
 * Routing broken
 *
 * Revision 1.10  2008/07/21 09:03:11  keinstein
 * Use symbolic enum values for device modes and device actions
 * move FlushUpdateUI() to Execute.cpp
 *
 * Revision 1.9  2008/06/02 16:02:00  keinstein
 * dont include Mutabor.rh since it is already included now
 * New interfache for IntCompDia
 * Set status dialog fields directly
 *
 * Revision 1.8  2008/03/11 10:37:34  keinstein
 * Holyday edition
 * put CM_xxx in an enum
 * use wx constants
 * document mutframe
 * some white space formattings
 * make route saving more system specific
 * many other fixes
 *
 *
 ********************************************************************
 * \defgroup runtime Runtime functions
 * \{
 ********************************************************************
 */
#include <memory.h>
#include <string.h>

#include "defs.hxx"

#include "global.hxx"

#include "hilfs.hxx"
#include "grafkern.hxx"

#include "runtime.hxx"
#include "execute.hxx"
//#include "Mutabor.rh"
#include <setjmp.h>

extern "C"
{

	bool RealTime = false;

	jmp_buf weiter_gehts_nach_compilerfehler;

	char pascal _export Compile(void *compDia, const wxChar *name) {
	  //		InitCompDia(compDia, name);
		
		if (!setjmp(weiter_gehts_nach_compilerfehler)) {
			loesche_syntax_speicher();
			init_yylex ();

			mutabor_programm_einlesen ( name );

			calc_declaration_numbers();

#if 0
			compDia->SetStatus(sd1,sd2,sd3,sd4,sd5,sd6);

			//	 show_line_number(-1);

			compDia->SetButtonText(_("Generating tables"));
			compDia->Refresh();
#endif
			mutabor_tabellen_generator();

#if 0
			compDia->SetButtonText(_("Translation successful !"));
			compDia->SetMessage(_("No error occured !"));
			compDia->Refresh();
#endif
			return 1;
		} else {
#if 0
			//show_line_number(-1);
			compDia->SetButtonText(_("Translation interrupted !"));

			compDia->SetMessage(Fmeldung);
			compDia->Refresh();
#endif
			return 0;
		}
	}

	UpdateUICallback* updateUIcallback;
  KeyChangedCallback* key_changed_callback;
  ParameterChangedCallback* anchor_changed_callback;
  ParameterChangedCallback* width_changed_callback;

  bool pascal _export
  Activate(bool realTime,
	   UpdateUICallback* callback,
	   KeyChangedCallback* key_change,
	   ParameterChangedCallback* anchor_change,
	   ParameterChangedCallback* width_change) {
		RealTime = realTime;
		GlobalReset();
		AktionenInit();
		updateUIcallback = callback;
		key_changed_callback = key_change;
		anchor_changed_callback = anchor_change;
		width_changed_callback = width_change;
#if 0
#if !defined(WX) || defined(__WXMSW__)

		if ( RealTime )
			timeBeginPeriod(1);

#endif
		bool ok = OutOpen();

		if ( ok && !InOpen() ) {
			ok = false;
			OutClose();
		}

		if ( !ok ) {
#if !defined(WX) || defined(__WXMSW__)
			if ( RealTime )
				timeEndPeriod(1);
#endif
			wxMessageBox(Fmeldung, _("Activation error"), wxOK | wxICON_ASTERISK );
			return false;
		}

		if ( RealTime )
			StartCurrentTime();
		else
			CurrentTime = 0;
#endif
		return true;
	}

	void pascal _export Stop() {
#if 0
		if ( RealTime )
			StopCurrentTime();

		InClose();

		OutClose();

#if !defined(WX) || defined(__WXMSW__)
		if ( RealTime )
			timeEndPeriod(1);

#endif
#endif
		GlobalReset();
	}


// NoRealTime - Aktionen

	void NRT_Play() {
#if 0
		// start all devices

		for (InDevice *In = InDevice::GetDeviceList(); In; In = In->GetNext())
			In->Play();

		// time slices
		bool Working = true;

		while ( Working ) {
			Working = false;

			for (InDevice *In = InDevice::GetDeviceList(); In; In = In->GetNext())
				if ( In->GetMode() == 1 && In->GetType() == DTMidiFile ) {
					((InMidiFile*)In)->IncDelta();
					Working = true;
				}

			CurrentTime.Notify();
		}

		// close all devices
		for (InDevice *In1 = InDevice::GetDeviceList(); In1; In1 = In1->GetNext())
			In1->Stop();

		InDevChanged = 1;
#endif
	}

	void pascal _export Panic() {
#if 0
		OutDevice *Out = OutDevice::GetDeviceList();
		while ( Out ) {
			Out->Panic();
			Out = Out->GetNext();
		}
#endif
	}

	bool pascal _export CheckNeedsRealTime() {
	  return false;
	  //return NeedsRealTime();
	}

	struct keyboard_ereignis *last;

	char pascal _export GetMutTag(char &isLogic, char *text, char *einsttext, char &key, int box) {
		if ( box != -1 )
			last = first_keyboard[box];
		else
			if ( last ) last = last->next;

		if ( !last ) return 0;

		key = last->taste;

		strncpy(text, last->aktion->name, 20);

		isLogic = ( last->the_logik_to_expand != NULL );

		if ( isLogic && last->the_logik_to_expand->einstimmungs_name )
			strncpy(einsttext, last->the_logik_to_expand->einstimmungs_name, 20);
		else
			strcpy(einsttext, "");

		return 1;
	}

	char pascal _export IsLogicKey(char key) {

		struct keyboard_ereignis *last = first_keyboard[aktuelles_keyboard_instrument];

		while ( last ) {
			if ( key == last->taste )
				return last->the_logik_to_expand != NULL;

			last = last->next;
		}

		return 2;
	}

	bool pascal _export KeyChanged(int box) {
		int flag = keys_changed[box];
		keys_changed[box] = 0;
		return flag;
	}

	ton_system last_tonsystem[MAX_BOX];

	bool pascal _export TSChanged(int box) {
		int flag = memcmp(&(last_tonsystem[box]),
		                  tonsystem[box],
		                  (2*sizeof(int)) + sizeof(long) +
		                  (tonsystem[box]->breite*
		                   sizeof(long)) );
		last_tonsystem[box] = *tonsystem[box];
		return flag;
	}

	bool pascal _export InDevicesChanged() {
	  return false;
#if 0
		char flag = InDevChanged;
		InDevChanged = 0;
		return flag;
#endif
	}

	struct instrument * lauf_instrument;

	char pascal _export GetChannels(char start, int &base, int &from, int &to, int &thru) {
		if ( start )
			lauf_instrument = list_of_config_instrumente;
		else if ( lauf_instrument )
			lauf_instrument = lauf_instrument -> next;

		if ( !lauf_instrument ) return 0;

		base = lauf_instrument -> midi_in;

		from = lauf_instrument -> midi_von;

		to 	 = lauf_instrument -> midi_bis;

		thru = lauf_instrument -> midi_umleit;

		return 1;
	}

	void pascal _export SetChannels(int base, int from, int to, int thru) {
		get_instrument_dekl (base, from, to, thru, &list_of_config_instrumente);
	}

	void pascal _export SetAktuellesKeyboardInstrument(int instr) {
		aktuelles_keyboard_instrument = instr;
	}

	int pascal _export GetAktuellesKeyboardInstrument() {
		return aktuelles_keyboard_instrument;
	}

// scan-Hilfsfunktionen ---------------------------------------------

#if 0
	bool GetELine(const wxString& p, size_t& i, wxString &s);

	DevType Str2DT(const wxString& type);

// aus p eine Zeile in s lesen, p wird verschoben
	bool GetLine(char **p, char *s) {
		if ( !p || !(*p)[0] )
			return false;

		while ( (*p)[0] == ' ' || (*p)[0] == '\n' || (*p)[0] == '\r' )
			*p = &(*p)[1];

		if ( !(*p)[0] )
			return false;

		char *p1 = *p;

		*p = strchr(p1, '\n');

		if ( !p )
			*p = &p1[strlen(p1)];

		int i = (*p)-p1;

		strncpy(s, p1, i);

		s[i] = 0;

		return true;
	}

#define GETLINE \
  if ( !GetELine(config, i, s) ) \
    return


// das nr-ste Output Device
// TODO Nr from 0 or 1?
	OutDevice *GetOut(int nr) {
		DEBUGLOG2(other,_T("Nr.: %d"),nr);

		if ( nr < 0 )
			return 0;

		OutDevice *Out = OutDevice::GetDeviceList();

		while ( Out ) {
			if (Out->GetDevId() == nr) break;

			Out = Out->GetNext();

			DEBUGLOG2(other,_T("Nr.: %d, Out: %x"),nr, Out);
		}

		return Out;
	}

#if 0
// Device aus einem String scannen
	void pascal _export ScanDevices(const wxString &config) {
		// Listen s‚Ä∞ubern

		if ( InDevice::GetDeviceList() ) {
			delete InDevice::GetDeviceList();
		}

		if ( OutDevices ) {
			delete OutDevices;
			OutDevices = 0;
		}

		// Zerlegen von config
		wxString s;

		size_t i = 0;

		GETLINE;

		while ( !s.StartsWith(_T("OUTPUT" ))) {
			GETLINE;
		}

		GETLINE;

		// Output lesen
		OutDevice **PreOut = &OutDevices;

		while ( !s.StartsWith(_T("INPUT") )) {
			wxChar Type[80], Name[400];
			int DevId, BendingRange;
#if (wxUSE_UNICODE || wxUSE_WCHAR_T)
			int test = SSCANF (s, _T("%ls \"%l[^\"]\" %d %d"), Type, Name, &DevId, &BendingRange);

			if ( test < 2 )
				test = SSCANF (s, _T("%ls %ls %d %d"), Type, Name, &DevId, &BendingRange);

#else
			int test = SSCANF (s, _T("%s \"%[^\"]\" %d %d"), Type, Name, &DevId, &BendingRange);

			if ( test < 2 )
				test = SSCANF (s, _T("%s %s %d %d"), Type, Name, &DevId, &BendingRange);

#endif
			if ( test < 2 ) {
				//3 ??
			}

			OutDevice *Out;

			switch ( Str2DT(Type) ) {

			case DTUnknown:
				std::cerr << "Unknown device: " << Type << std::endl;

				//3 ??

			case DTGis:
				Out = new OutGis(Name);

				break;

			case DTMidiPort:
				Out = new OutMidiPort(Name, DevId, BendingRange);

				break;

			case DTMidiFile:
				Out = new OutMidiFile(Name, DevId, BendingRange);

				break;
			}

			*PreOut = Out;

			PreOut = &(Out->Next);
			GETLINE;
		}

		GETLINE;

		// Input lesen

		while ( 1 ) {
			// Device lesen
			wxChar Type[80], Name[400];
			int DevId = -1;
#if (wxUSE_UNICODE || wxUSE_WCHAR_T)
			int test = SSCANF (s, _T("%ls \"%l[^\"]\" %d"), Type, Name, &DevId);

			if ( test < 2 )
				test = SSCANF (s, _T("%ls %ls %d"), Type, Name, &DevId);

#else
			int test = SSCANF (s, _T("%s \"%[^\"]\" %d"), Type, Name, &DevId);

			if ( test < 2 )
				test = SSCANF (s, _T("%s %s %d"), Type, Name, &DevId);

#endif
			if ( test < 2 ) {
				//3 ??
			}

			InDevice *In;

			switch ( Str2DT(muT(Type)) ) {

			case DTUnknown:
				//3 ??

			case DTGis:
				In = new InGis(Name, _T("GIS"));

				break;

			case DTMidiPort:
				In = new InMidiPort(Name, DevId);

				break;

			case DTMidiFile:
				In = new InMidiFile(Name, 0);

				break;
			}


			GETLINE;
			// Routen lesen

			while ( Str2DT(s) == DTUnknown ) {
				// Route lesen
				wxChar Type[40];
				int IFrom = 0, ITo = 0, Box = 0, BoxActive = 0, OutDev = -1, OFrom = -1, OTo = -1, ONoDrum = 1;
#if (wxUSE_UNICODE || wxUSE_WCHAR_T)
				test = SSCANF(s, _("%ls %d %d %d %d %d %d %d %d"),
				              Type, &IFrom, &ITo, &Box, &BoxActive, &OutDev, &OFrom, &OTo, &ONoDrum);
#else
				test = SSCANF(s, _("%s %d %d %d %d %d %d %d %d"),
				              Type, &IFrom, &ITo, &Box, &BoxActive, &OutDev, &OFrom, &OTo, &ONoDrum);
#endif

				if ( test < 2 ) {
					//3 ??
				}

				if ( Box == -2 ) // zur Sicherheit
					BoxActive = 0;

				In->AddRoute(new Route(Str2RT(Type), IFrom, ITo, Box, BoxActive, GetOut(OutDev), OFrom, OTo, ONoDrum));

				GETLINE;
			}
		}
	}

#endif

// Timerdaten
	void pascal _export GetTimerData(UINT &min, UINT &max) {
#if !defined(WX) || defined(__WXMSW__)
		TIMECAPS TimeCaps;
		timeGetDevCaps(&TimeCaps, sizeof(TIMECAPS));
		min = TimeCaps.wPeriodMin;
		max = TimeCaps.wPeriodMax;
#else
		//TODO
#endif
	}
#endif

} // Extern C

/* \} */
