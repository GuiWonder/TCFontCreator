using System;
using System.IO;
using System.Windows.Forms;
using System.Xml;

namespace TCFontCreator
{
    public partial class FormMain : Form
    {
        public FormMain(string[] args)
        {
            showCMD = args.Length > 0 && args[0].ToLower() == "cmd";
            InitializeComponent();
        }

        public string lan;
        System.Collections.Generic.List<string> listlan;
        public System.Collections.Generic.List<string> listMsg;
        public System.Collections.Generic.List<string> addfonts;
        string cfgFile;
        private readonly bool showCMD;
        private string exeffpy;
        private string exepy;
        private string path;
        private string fileout;
        private bool useotfcc;
        private System.Threading.Thread thRun;
        private string err;
        private string outinfo;
        private string cmdline;

        private void FormMain_Load(object sender, EventArgs e)
        {
            CheckForIllegalCrossThreadCalls = false;
            tabControl1.SelectedIndexChanged += TabControl1_SelectedIndexChanged;
            comboBoxMulti.SelectedIndexChanged += ComboBoxMulti_SelectedIndexChanged;
            comboBoxMg.SelectedIndexChanged += ComboBoxMg_SelectedIndexChanged;
            ReadDeFault();
            panel1.Enabled = checkBoxInfo.Checked;
            comboBoxSys.SelectedIndex = 0;
            comboBoxLan.SelectedIndex = 0;
            comboBoxMg.SelectedIndex = 0;
            comboBoxApp.SelectedIndex = 0;
            comboBoxVar.SelectedIndex = 0;
            comboBoxMulti.SelectedIndex = 1;
            addfonts = new System.Collections.Generic.List<string>();
            path = AppDomain.CurrentDomain.BaseDirectory;
            cfgFile = path + "config.xml";
            ReadCfg();
            SetLan();
            comboBoxLan.SelectedIndexChanged += ComboBoxLan_SelectedIndexChanged;
            buttonFontsList.Click += ButtonFontsList_Click;
            textBoxFFPth.LostFocus += TextBoxFFPth_LostFocus;
            textBoxPypth.LostFocus += TextBoxFFPth_LostFocus;
            linkLabelPy.LinkClicked += LinkLabelPy_LinkClicked;
            linkLabelFF.LinkClicked += LinkLabelFF_LinkClicked;
        }

        private void ButtonStart_Click(object sender, EventArgs e)
        {
            string filein = textBoxIn.Text.Trim();
            string filein2 = textBoxIn2.Text.Trim();
            fileout = textBoxOut.Text.Trim();

            if ((!System.IO.File.Exists(filein)) || (!System.IO.File.Exists(filein2) && tabControl1.SelectedIndex == 1 && comboBoxMg.SelectedIndex == 2) || string.IsNullOrWhiteSpace(fileout))
            {
                MessageBox.Show(this, listMsg[1], "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (tabControl1.SelectedIndex == 1 && comboBoxMg.SelectedIndex == 0 && addfonts.Count < 1)
            {
                MessageBox.Show(this, listMsg[9], "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            useotfcc = comboBoxApp.SelectedIndex == 0;
            SetExec();
            if (useotfcc && !System.IO.File.Exists(exepy))
            {
                MessageBox.Show(this, "未找到 Python，" + listMsg[2], "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (!useotfcc && !System.IO.File.Exists(exeffpy))
            {
                MessageBox.Show(this, "未找到 FontForge，" + listMsg[2], "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string pyfile = useotfcc ? path + "converto.py" : path + "convertf.py";
            pyfile = pyfile.Replace('\\', '/');
            string args = $"\"{pyfile}\" -i \"{filein}\" -o \"{fileout}\"";

            string runmd = "";

            if (tabControl1.SelectedIndex == 0)
            {
                runmd = tabControl1.SelectedIndex.ToString() + comboBoxSys.SelectedIndex.ToString() + comboBoxMulti.SelectedIndex.ToString() + comboBoxVar.SelectedIndex.ToString();
            }
            else if (tabControl1.SelectedIndex == 1)
            {
                runmd = tabControl1.SelectedIndex.ToString() + comboBoxMg.SelectedIndex.ToString();
            }
            args += " -wk " + runmd;
            if (tabControl1.SelectedIndex == 0 && checkBoxYitizi.Checked)
            {
                args += " -v";
            }

            if (checkBoxInfo.Checked)
            {
                if (string.IsNullOrWhiteSpace(textBoxName.Text))
                {
                    MessageBox.Show(this, listMsg[3], "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                else
                {
                    args += $" -n \"{textBoxName.Text}\"";
                    if (!string.IsNullOrWhiteSpace(textBoxTCName.Text))
                    {
                        args += $" -n1 \"{textBoxTCName.Text}\"";
                    }
                    if (!string.IsNullOrWhiteSpace(textBoxSCName.Text))
                    {
                        args += $" -n2 \"{textBoxSCName.Text}\"";
                    }
                    if (!string.IsNullOrWhiteSpace(textBoxVersi.Text))
                    {
                        args += $" -n3 \"{textBoxVersi.Text}\"";
                    }
                }
            }
            if (tabControl1.SelectedIndex == 1)
            {
                if (comboBoxMg.SelectedIndex == 0)
                {
                    foreach (var item in addfonts)
                    {
                        args += " -i2 \"" + item + "\"";
                    }
                }
                else if (comboBoxMg.SelectedIndex == 2)
                {
                    args += " -i2 \"" + filein2 + "\"";
                }
                if (checkBoxIH.Checked)
                {
                    args += " -ih";
                }
            }

            if (!useotfcc)
            {
                exeffpy = exeffpy.Replace("\\", "/");
                string bin = exeffpy.Substring(0, exeffpy.LastIndexOf('/'));
                string ffpath = bin.Substring(0, bin.LastIndexOf('/'));
                cmdline = $"set \"PYTHONHOME={ffpath}\"&\"{exeffpy}\" {args}";
            }
            else
            {
                cmdline = $"\"{exepy}\" {args}";
            }
            if (!showCMD)
            {
                cmdline += "&exit";
            }

            tabControl1.Enabled = false;
            Cursor = Cursors.WaitCursor;
            Text = listMsg[4];
            err = "";
            outinfo = "";
            thRun = new System.Threading.Thread(ThRun)
            {
                IsBackground = true
            };
            thRun.Start();
        }

        private void ThRun()
        {
            using (System.Diagnostics.Process p = new System.Diagnostics.Process())
            {
                p.StartInfo.FileName = "cmd";
                fileout = fileout.Replace('\\', '/');
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = !showCMD;
                p.StartInfo.RedirectStandardError = !showCMD;
                p.StartInfo.RedirectStandardOutput = !showCMD;
                p.StartInfo.RedirectStandardInput = true;
                p.Start();
                p.StandardInput.WriteLine(cmdline);
                if (!showCMD)
                {
                    p.ErrorDataReceived += P_ErrorDataReceived;
                    p.OutputDataReceived += P_OutputDataReceived;
                    p.BeginErrorReadLine();
                    p.BeginOutputReadLine();
                }
                p.WaitForExit();
                p.Close();
            }
            Invoke(new Action(delegate
            {
                tabControl1.Enabled = true;
                Cursor = Cursors.Default;
                Text = " 已完成";
                if (System.IO.File.Exists(fileout))
                {
                    if (outinfo.EndsWith("Finished!"))
                    {
                        if (string.IsNullOrWhiteSpace(err))
                        {
                            MessageBox.Show(this, "成功！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        }
                        else
                        {
                            MessageBox.Show(this, listMsg[5] + "\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                    else if (!string.IsNullOrWhiteSpace(err))
                    {
                        MessageBox.Show(this, listMsg[6] + "\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                    else
                    {
                        MessageBox.Show(this, listMsg[7], "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
                else
                {
                    MessageBox.Show(this, listMsg[6] + "\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }));
        }

        private void SetExec()
        {
            exeffpy = textBoxFFPth.Text;
            if (string.IsNullOrWhiteSpace(exeffpy))
                exeffpy = "FontForgeBuilds/bin/ffpython.exe";
            if (System.IO.File.Exists(path + exeffpy))
                exeffpy = path + exeffpy;

            exepy = textBoxPypth.Text;
            if (string.IsNullOrWhiteSpace(exepy))
                exepy = "python/python.exe";
            if (System.IO.File.Exists(path + exepy))
                exepy = path + exepy;

            if (!System.IO.File.Exists(exeffpy))
            {
                if (System.IO.File.Exists("C:/Program Files (x86)/FontForgeBuilds/bin/ffpython.exe"))
                {
                    exeffpy = "C:/Program Files (x86)/FontForgeBuilds/bin/ffpython.exe";
                }
                else if (System.IO.File.Exists("C:/Program Files/FontForgeBuilds/bin/ffpython.exe"))
                {
                    exeffpy = "C:/Program Files/FontForgeBuilds/bin/ffpython.exe";
                }
            }
        }

        private void P_OutputDataReceived(object sender, System.Diagnostics.DataReceivedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(e.Data))
            {
                outinfo = e.Data;
            }
        }

        private void P_ErrorDataReceived(object sender, System.Diagnostics.DataReceivedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(e.Data) && (e.Data.Contains("Error") || e.Data.Contains("ERROR") || e.Data.Contains("[Errno")) && !e.Data.Contains("raise"))
            {
                err += e.Data + "\r\n";
            }
        }

        private void LinkLabelFF_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            OpenFileDialog openFileDialogexe = new OpenFileDialog
            {
                Filter = "ffpython|ffpython.exe|All Files|*.*"
            };
            if (openFileDialogexe.ShowDialog() == DialogResult.OK)
            {
                textBoxFFPth.Text = openFileDialogexe.FileName;
            }
        }

        private void LinkLabelPy_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            OpenFileDialog openFileDialogexe = new OpenFileDialog
            {
                Filter = "python|python.exe|All Files|*.*"
            };
            if (openFileDialogexe.ShowDialog() == DialogResult.OK)
            {
                textBoxPypth.Text = openFileDialogexe.FileName;
            }

        }

        private void ButtonFontsList_Click(object sender, EventArgs e)
        {
            using (FontsList ftlist = new FontsList(this))
            {
                if (ftlist.ShowDialog() == DialogResult.OK)
                {
                    buttonFontsList.Text = $"已添加 {addfonts.Count} {listMsg[0]}";
                }
            }
        }

        private void ComboBoxMg_SelectedIndexChanged(object sender, EventArgs e)
        {
            label10.Enabled = comboBoxMg.SelectedIndex == 0;
            buttonFontsList.Enabled = comboBoxMg.SelectedIndex == 0;
            labeli2.Enabled = comboBoxMg.SelectedIndex == 2;
            textBoxIn2.Enabled = comboBoxMg.SelectedIndex == 2;
            linkLabelIn2.Enabled = comboBoxMg.SelectedIndex == 2;
        }

        private void TextBoxFFPth_LostFocus(object sender, EventArgs e) => WriteCfg();

        private void ReadCfg()
        {
            if (!System.IO.File.Exists(cfgFile))
            {
                return;
            }
            try
            {
                XmlDocument doc = new XmlDocument();
                doc.Load(cfgFile);
                comboBoxLan.SelectedIndex = int.Parse(doc.SelectSingleNode("Config/Setting/LanID").InnerText);
                string pyrd = doc.SelectSingleNode("Config/Setting/PyPath").InnerText;
                string ffrd = doc.SelectSingleNode("Config/Setting/FFPath").InnerText;
                if (!string.IsNullOrWhiteSpace(pyrd))
                {
                    textBoxPypth.Text = pyrd;
                }
                if (!string.IsNullOrWhiteSpace(ffrd))
                {
                    textBoxFFPth.Text = ffrd;
                }
            }
            catch (Exception)
            {
            }
        }

        private void WriteCfg()
        {
            XmlDocument doc = new XmlDocument();
            XmlDeclaration dec = doc.CreateXmlDeclaration("1.0", "utf-8", null);
            doc.AppendChild(dec);
            XmlElement cfg = doc.CreateElement("Config");
            doc.AppendChild(cfg);
            XmlElement set = doc.CreateElement("Setting");
            cfg.AppendChild(set);
            XmlElement lanid = doc.CreateElement("LanID");
            lanid.InnerText = comboBoxLan.SelectedIndex.ToString();
            set.AppendChild(lanid);
            XmlElement pypth = doc.CreateElement("PyPath");
            pypth.InnerText = textBoxPypth.Text;
            set.AppendChild(pypth);
            XmlElement ffpth = doc.CreateElement("FFPath");
            ffpth.InnerText = textBoxFFPth.Text;
            set.AppendChild(ffpth);
            doc.Save(cfgFile);
        }

        private void ComboBoxMulti_SelectedIndexChanged(object sender, EventArgs e) => comboBoxVar.Enabled = comboBoxMulti.SelectedIndex != 3;

        private void ComboBoxLan_SelectedIndexChanged(object sender, EventArgs e)
        {
            SetLan();
            WriteCfg();
        }

        private void SetLan()
        {
            string[] lans = { "landef", "lansc", "lantw" };
            lan = lans[comboBoxLan.SelectedIndex] + ".lan";

            string filelan = path + "locales/" + lan;
            if (!System.IO.File.Exists(filelan))
            {
                return;
            }
            StreamReader sr = new StreamReader(filelan);
            listlan = new System.Collections.Generic.List<string>();
            while (!sr.EndOfStream)
            {
                listlan.Add(sr.ReadLine());
            }
            if (listlan.Count < 45)
            {
                return;
            }
            Text = " " + listlan[0];
            tabPage1.Text = listlan[1];
            label7.Text = listlan[2];
            comboBoxSys.Items[0] = listlan[3];
            comboBoxSys.Items[1] = listlan[4];
            buttonStart.Text = listlan[5];
            labeli1.Text = listlan[6];
            linkLabelOut.Text = listlan[7];
            linkLabelIn2.Text = listlan[7];
            linkLabelIn.Text = listlan[7];
            linkLabelFF.Text = listlan[7];
            linkLabelPy.Text = listlan[7];
            labelo.Text = listlan[8];
            label8.Text = listlan[9];
            checkBoxYitizi.Text = listlan[10];
            labelMilti.Text = listlan[11];
            comboBoxMulti.Items[0] = listlan[12];
            comboBoxMulti.Items[1] = listlan[13];
            comboBoxMulti.Items[2] = listlan[14];
            comboBoxMulti.Items[3] = listlan[15];
            label1.Text = listlan[16];
            comboBoxVar.Items[0] = listlan[17];
            comboBoxVar.Items[1] = listlan[18];
            comboBoxVar.Items[2] = listlan[19];
            comboBoxVar.Items[3] = listlan[20];
            checkBoxInfo.Text = listlan[21];
            label3.Text = listlan[22];
            tabPage2.Text = listlan[23];
            comboBoxMg.Items[0] = listlan[24];
            comboBoxMg.Items[1] = listlan[25];
            comboBoxMg.Items[2] = listlan[26];
            label10.Text = listlan[27];
            buttonFontsList.Text = listlan[28];
            labeli2.Text = listlan[29];
            tabPage3.Text = listlan[30];
            label12.Text = listlan[31];
            label13.Text = "Fontforge " + listlan[32];
            label11.Text = "Python " + listlan[32];
            label14.Text = listlan[33];
            listMsg[0] = listlan[34];
            listMsg[1] = listlan[35];
            listMsg[2] = listlan[36];
            listMsg[3] = listlan[37];
            listMsg[4] = listlan[38];
            listMsg[5] = listlan[39];
            listMsg[6] = listlan[40];
            listMsg[7] = listlan[41];
            listMsg[8] = $"{listlan[42]}|*.ttf;*.otf|{listlan[43]}|*.*";
            listMsg[9] = listlan[44];
            openFileDialog1.Filter = listMsg[8];
            saveFileDialog1.Filter = listMsg[8];
            if (addfonts.Count > 0)
            {
                buttonFontsList.Text = $"已添加 {addfonts.Count} {listMsg[0]}";
            }
        }

        private void ReadDeFault()
        {
            listMsg = new System.Collections.Generic.List<string>
            {
                "個字體，點擊修改",
                "文件無效，請重新選擇。",
                "請在設定中重新填寫程序路徑。",
                "「字體名稱(英)」不能爲空。",
                "正在處理，請稍後...",
                "出現錯誤！",
                "失敗！",
                "程序執行完畢。",
                "字體文件|*.ttf;*.otf|所有文件|*.*",
                "請添加補入的字體。"
            };
        }

        private void TabControl1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (tabControl1.SelectedIndex == 0)
            {
                groupBox1.Controls.Add(labeli1);
                groupBox1.Controls.Add(labelo);
                groupBox1.Controls.Add(label7);
                groupBox1.Controls.Add(textBoxIn);
                groupBox1.Controls.Add(textBoxOut);
                groupBox1.Controls.Add(linkLabelIn);
                groupBox1.Controls.Add(linkLabelOut);
                groupBox1.Controls.Add(buttonStart);
                groupBox1.Controls.Add(label8);
                groupBox1.Controls.Add(comboBoxApp);
                groupBox3.Controls.Add(checkBoxInfo);
                groupBox3.Controls.Add(panel1);

            }
            else if (tabControl1.SelectedIndex == 1)
            {
                groupBox2.Controls.Add(labeli1);
                groupBox2.Controls.Add(labelo);
                groupBox2.Controls.Add(label7);
                groupBox2.Controls.Add(textBoxIn);
                groupBox2.Controls.Add(textBoxOut);
                groupBox2.Controls.Add(linkLabelIn);
                groupBox2.Controls.Add(linkLabelOut);
                groupBox2.Controls.Add(buttonStart);
                groupBox2.Controls.Add(label8);
                groupBox2.Controls.Add(comboBoxApp);
                groupBox4.Controls.Add(checkBoxInfo);
                groupBox4.Controls.Add(panel1);
            }
        }

        private void FormMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (thRun != null && thRun.IsAlive)
            {
                e.Cancel = true;
                //if (MessageBox.Show("有任務正在工作，確定要放棄當前任務嗎？", "提示", MessageBoxButtons.YesNo, MessageBoxIcon.Exclamation, MessageBoxDefaultButton.Button2) == DialogResult.Yes)
                //{
                //    Environment.Exit(0);
                //}
                //else
                //{
                //    e.Cancel = true;
                //}
            }
        }

        private void CheckBoxInfo_CheckedChanged(object sender, EventArgs e) => panel1.Enabled = checkBoxInfo.Checked;

        private void TextBox_DragEnter(object sender, DragEventArgs e) => e.Effect = e.Data.GetDataPresent(DataFormats.FileDrop) ? DragDropEffects.All : DragDropEffects.None;

        private void TextBox_DragDrop(object sender, DragEventArgs e) => ((TextBox)sender).Text = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();

        private void ComboBoxSys_SelectedIndexChanged(object sender, EventArgs e) => panelTC.Enabled = comboBoxSys.SelectedIndex == 0;

        private void LinkLabelIn_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                textBoxIn.Text = openFileDialog1.FileName;
            }
        }

        private void LinkLabelIn2_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                textBoxIn2.Text = openFileDialog1.FileName;
            }
        }

        private void LinkLabelOut_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                textBoxOut.Text = saveFileDialog1.FileName;
            }
        }

        private void LinkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            System.Diagnostics.Process.Start("https://github.com/GuiWonder/TCFontCreator");
        }
    }
}
