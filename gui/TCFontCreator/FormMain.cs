using System;
using System.Windows.Forms;

namespace TCFontCreator
{
    public partial class FormMain : Form
    {
        public FormMain(string[] args)
        {
            showCMD = args.Length > 0 && args[0].ToLower() == "cmd";
            InitializeComponent();
        }

        private readonly bool showCMD;
        private string exeffpy;
        private string exepy;
        private string path;
        private string fileout;
        private string args;
        private bool otcff;
        private System.Threading.Thread thRun;
        private string err;
        private string outinfo;

        private void FormMain_Load(object sender, EventArgs e)
        {
            comboBoxSys.SelectedIndex = 0;
            comboBoxApp.SelectedIndex = 0;
            comboBoxVar.SelectedIndex = 0;
            comboBoxMulti.SelectedIndex = 1;
            panel1.Enabled = checkBoxInfo.Checked;
            CheckForIllegalCrossThreadCalls = false;
        }

        private void SetExec()
        {
            exeffpy = path + "FontForgeBuilds/bin/ffpython.exe";
            exepy = path + "python/python.exe";
            if (System.IO.File.Exists("appdata"))
            {
                string[] str = System.IO.File.ReadAllLines("appdata");
                foreach (string item in str)
                {
                    string line = item.Trim();
                    if (!line.StartsWith("#") && line.Contains("="))
                    {
                        string[] finfo = line.Split('=');
                        if (finfo[0].Trim().ToLower() == "fontforge")
                        {
                            string f = finfo[1].Trim().Replace("\\", "/");
                            if (f.ToLower().EndsWith("fontforge.exe"))
                            {
                                string file = f.Substring(0, f.LastIndexOf('/') + 1) + "ffpython.exe";
                                if (System.IO.File.Exists(file))
                                {
                                    exeffpy = file;
                                }
                            }
                            else if (f.ToLower().EndsWith("ffpython.exe"))
                            {
                                if (System.IO.File.Exists(f))
                                {
                                    exeffpy = f;
                                }
                            }
                        }
                        else if (finfo[0].Trim().ToLower() == "python")
                        {
                            string f = finfo[1].Trim().Replace("\\", "/");
                            if (System.IO.File.Exists(f))
                            {
                                exepy = f;
                            }
                        }
                    }
                }
            }
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
            //if (!System.IO.File.Exists(exepy) && System.IO.File.Exists(exeffpy))
            //{
            //    exepy = exeffpy;
            //}
        }

        private void ButtonStart_Click(object sender, EventArgs e)
        {
            path = AppDomain.CurrentDomain.BaseDirectory;
            string filein = textBoxIn.Text.Trim();
            string filein2 = textBoxIn2.Text.Trim();
            fileout = textBoxOut.Text.Trim();
            otcff = comboBoxApp.SelectedIndex == 0;
            string stmode;
            switch (comboBoxSys.SelectedIndex)
            {
                case 0:
                    stmode = "st";
                    break;
                case 1:
                    stmode = "var";
                    break;
                case 2:
                    stmode = "sat";
                    break;
                case 3:
                    stmode = "faf";
                    break;
                case 4:
                    stmode = "jt";
                    break;
                case 5:
                    stmode = "ts";
                    break;
                default:
                    stmode = "st";
                    break;
            }
            if (stmode == "st")
            {
                if (comboBoxVar.SelectedIndex == 1)
                {
                    stmode += "tw";
                }
                else if (comboBoxVar.SelectedIndex == 2)
                {
                    stmode += "hk";
                }
                else if (comboBoxVar.SelectedIndex == 3)
                {
                    stmode += "cl";
                }
                if (comboBoxMulti.SelectedIndex == 1)
                {
                    stmode += ".s";
                }
                else if (comboBoxMulti.SelectedIndex == 2)
                {
                    stmode += ".m";
                }
            }
            SetExec();
            if ((!System.IO.File.Exists(filein)) || (!System.IO.File.Exists(filein2) && (stmode == "sat" || stmode == "faf")) || string.IsNullOrWhiteSpace(fileout))
            {
                MessageBox.Show(this, "文件無效，請重新選擇。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (otcff && !System.IO.File.Exists(exepy))
            {
                if (System.IO.File.Exists(exeffpy))
                {
                    if (MessageBox.Show(this, "未能找到 Python,要使用 FontForge 所附帶的 Python 模塊嗎？可以在 appdata 文件中設置 python.exe 的路徑。", "提示", MessageBoxButtons.YesNo, MessageBoxIcon.Question, MessageBoxDefaultButton.Button1) == DialogResult.Yes)
                    {
                        exepy = exeffpy;
                    }
                    else
                    {
                        return;
                    }
                }
                else
                {
                    MessageBox.Show(this, "未能找到 Python 或 FontForge,請在 appdata 文件中設置 python.exe 或 fontforge.exe 的路徑。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }

            if (!otcff && !System.IO.File.Exists(exeffpy))
            {
                MessageBox.Show(this, "未能找到 FontForge,請在 appdata 文件中設置 fontforge.exe 的路徑。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (checkBoxInfo.Checked && string.IsNullOrWhiteSpace(textBoxName.Text))
            {
                MessageBox.Show(this, "您需要輸入字體名稱。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (stmode == "sat" || stmode == "faf")
            {
                filein = $"-i \"{filein}\" -i2 \"{filein2}\"";
            }
            else
            {
                filein = $"-i \"{filein}\"";
            }
            string pyfile = otcff ? path + "converto.py" : path + "convertf.py";
            pyfile = pyfile.Replace('\\', '/');
            args = $"\"{pyfile}\" {filein} -o \"{fileout}\" -wk {stmode}";
            if (stmode != "var" && checkBoxYitizi.Checked)
            {
                args += " -v";
            }
            if (checkBoxInfo.Checked && !string.IsNullOrWhiteSpace(textBoxName.Text))
            {
                args += $" -n \"{textBoxName.Text}\"";
                if (!string.IsNullOrWhiteSpace(textBoxTCName.Text))
                {
                    args += $" -ntc \"{textBoxTCName.Text}\"";
                }
                if (!string.IsNullOrWhiteSpace(textBoxSCName.Text))
                {
                    args += $" -nsc \"{textBoxSCName.Text}\"";
                }
                if (!string.IsNullOrWhiteSpace(textBoxVersi.Text))
                {
                    args += $" -vn \"{textBoxVersi.Text}\"";
                }
            }

            panelMain.Enabled = false;
            Cursor = Cursors.WaitCursor;
            Text = "正在處理，請耐心等待...";
            err = "";
            outinfo = "";
            thRun = new System.Threading.Thread(ThRun);
            thRun.IsBackground = true;
            thRun.Start();
        }

        private void ThRun()
        {
            using (System.Diagnostics.Process p = new System.Diagnostics.Process())
            {
                p.StartInfo.FileName = "cmd";
                string pyfile = otcff ? path + "covotfcc.py" : path + "covff.py";
                fileout = fileout.Replace('\\', '/');
                string bin = exeffpy.Substring(0, exeffpy.LastIndexOf('/'));
                string ffpath = bin.Substring(0, bin.LastIndexOf('/'));
                string arg1 = (otcff && exeffpy != exepy) ? "" : $"set \"PYTHONHOME={ffpath}\"&";
                string runexe = (otcff && exeffpy != exepy) ? exepy : exeffpy;
                string arg2 = $"\"{runexe}\" {args}";
                string arg3 = showCMD ? "" : "&exit";
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = !showCMD;
                p.StartInfo.RedirectStandardError = !showCMD;
                p.StartInfo.RedirectStandardOutput = !showCMD;
                p.StartInfo.RedirectStandardInput = true;
                p.Start();
                p.StandardInput.WriteLine($"{arg1}{arg2}{arg3}");
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
                panelMain.Enabled = true;
                Cursor = Cursors.Default;
                Text = " 中文字體簡繁處理工具";
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
                            MessageBox.Show(this, "出現錯誤！\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                    else if (!string.IsNullOrWhiteSpace(err))
                    {
                        MessageBox.Show(this, "失敗！\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                    else
                    {
                        MessageBox.Show(this, "處理完畢，但無法確定是否成功。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }
                else
                {
                    MessageBox.Show(this, "失敗！\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);

                }
            }));
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

        private void ComboBoxSys_SelectedIndexChanged(object sender, EventArgs e)
        {
            checkBoxYitizi.Enabled = comboBoxSys.SelectedIndex != 1;
            panelTC.Enabled = comboBoxSys.SelectedIndex == 0;
            labeli2.Enabled = comboBoxSys.SelectedIndex == 2 || comboBoxSys.SelectedIndex == 3;
            textBoxIn2.Enabled = comboBoxSys.SelectedIndex == 2 || comboBoxSys.SelectedIndex == 3;
            linkLabelIn2.Enabled = comboBoxSys.SelectedIndex == 2 || comboBoxSys.SelectedIndex == 3;
        }

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
