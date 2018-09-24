// PS4Macro (File: Classes/MacroPlayer.cs)
//
// Copyright (c) 2017 Komefai
//
// Visit http://komefai.com for more information
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

using PS4RemotePlayInterceptor;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;


namespace PS4Macro.Classes
{
    public delegate void MacroLapEnterHandler(object sender);

    public class MacroPlayer : INotifyPropertyChanged
    {
        #region INotifyPropertyChanged
        public event PropertyChangedEventHandler PropertyChanged;
        private void NotifyPropertyChanged(string propertyName = "")
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        #endregion

        #region Properties
        private bool m_IsPlaying = false;
        public bool IsPlaying
        {
            get { return m_IsPlaying; }
            private set
            {
                if (value != m_IsPlaying)
                {
                    m_IsPlaying = value;
                    NotifyPropertyChanged("IsPlaying");
                }
            }
        }

        private bool m_IsPaused = false;
        public bool IsPaused
        {
            get { return m_IsPaused; }
            private set
            {
                if (value != m_IsPaused)
                {
                    m_IsPaused = value;
                    NotifyPropertyChanged("IsPaused");
                }
            }
        }

        private bool m_IsRecording = false;
        public bool IsRecording
        {
            get { return m_IsRecording; }
            private set
            {
                if (value != m_IsRecording)
                {
                    m_IsRecording = value;
                    NotifyPropertyChanged("IsRecording");
                }
            }
        }

        private int m_CurrentTick = 0;
        public int CurrentTick
        {
            get { return m_CurrentTick; }
            private set
            {
                if (value != m_CurrentTick)
                {
                    m_CurrentTick = value;
                    NotifyPropertyChanged("CurrentTick");
                }
            }
        }

        private List<DualShockState> m_Sequence = new List<DualShockState>();
        public List<DualShockState> Sequence
        {
            get { return m_Sequence; }
            set
            {
                if (value != m_Sequence)
                {
                    m_Sequence = value;
                    NotifyPropertyChanged("Sequence");
                }
            }
        }
        #endregion

        #region Events
        public event MacroLapEnterHandler LapEnter;
        #endregion

        /* Constructor */
        public MacroPlayer()
        {
            IsPlaying = false;
            IsPaused = false;
            IsRecording = false;
            CurrentTick = 0;
            Sequence = new List<DualShockState>();
            
            run_cv();
        }
        
        public void Play()
        {
            IsPlaying = true;
            IsPaused = false;
        }

        public void Pause()
        {
            IsPlaying = true;
            IsPaused = true;
        }

        public void Stop()
        {
            IsPlaying = false;
            IsPaused = false;
            CurrentTick = 0;
        }

        public void Record()
        {
            IsRecording = !IsRecording;
        }

        public void Clear()
        {
            Sequence = new List<DualShockState>();
            CurrentTick = 0;
        }

        public void LoadFile(string path)
        {
            Sequence = DualShockState.Deserialize(path);
        }

        public void SaveFile(string path)
        {
            DualShockState.Serialize(path, Sequence);
        }

        public void Run(ref DualShockState state)
        {
        }
        

        double xPressed = 0;
        double rightPressed = 0;
        double downPressed = 0;
        double oPressed = 0;
        Stopwatch deltatime = new Stopwatch();
        
        public void OnReceiveData(ref DualShockState state)
        {
            state.Cross = xPressed > 0;
            state.Circle = oPressed > 0;
            state.DPad_Right = rightPressed > 0;
            state.DPad_Down = downPressed > 0;

            deltatime.Stop();
            double dt = deltatime.ElapsedMilliseconds / 1000.0;
            xPressed -= dt;
            rightPressed -= dt;
            downPressed -= dt;
            oPressed -= dt;

            deltatime.Reset();
            deltatime.Start();
        }

        const double INPUT_LENGTH = 0.2;

        private void OutputHandler(object sender, DataReceivedEventArgs e)
        {
            if (e.Data != null)
            {
                System.Diagnostics.Debug.WriteLine(e.Data);

                switch (e.Data)
                {
                    case  "press x":
                        xPressed = INPUT_LENGTH;
                        break;

                    case "press right":
                        rightPressed = INPUT_LENGTH;
                        break;

                    case "press o":
                        oPressed = INPUT_LENGTH;
                        break;

                    case "press down":
                        downPressed = INPUT_LENGTH;
                        break;
                }
            }
        }
        
        private void run_cv()
        {
            Console.WriteLine("initializing cv");
            string python = @"C:\Program Files\Python36\python.exe";

            // python app to call
            string myPythonApp = "run.py";
            // Create new process start info
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo(python);

            // make sure we can read the output from stdout
            myProcessStartInfo.UseShellExecute = false;
            myProcessStartInfo.RedirectStandardOutput = true;
            myProcessStartInfo.CreateNoWindow = true;
            myProcessStartInfo.Arguments = myPythonApp;

            Process myProcess = new Process();
            // assign start information to the process
            myProcess.StartInfo = myProcessStartInfo;
            myProcess.EnableRaisingEvents = true;
            myProcess.OutputDataReceived += OutputHandler;

            // start the process
            myProcess.Start();
            myProcess.BeginOutputReadLine();
        }
    }
}