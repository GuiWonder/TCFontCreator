using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Media;
using System.Reflection;
using System.Runtime.Remoting.Messaging;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Xml;

namespace TCFontCreator
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        readonly string vercode = "20250303";
        readonly string CFGFILE;
        readonly bool DEBUG;
        readonly Button[] ps;
        private readonly Microsoft.Win32.OpenFileDialog openFileDialog = new Microsoft.Win32.OpenFileDialog();
        private readonly Microsoft.Win32.SaveFileDialog saveFileDialog = new Microsoft.Win32.SaveFileDialog();
        private System.Threading.Thread thread;
        readonly string path;
        private readonly IDictionary<string, string> CLan = new Dictionary<string, string>();
        private readonly IDictionary<string, string> FLan = new Dictionary<string, string>();

        public MainWindow()
        {
            InitializeComponent();
            ps = new Button[] { p1, p2, p3 };
            foreach (TabItem tbit in tab1.Items)
            {
                tbit.Visibility = Visibility.Hidden;
            }
            P_Click(p1, null);
            DisableElement();
            Closing += MainWindow_Closing;

            cbLan.SelectedIndex = 0;
            Assembly asb = GetType().Assembly;
            path = AppDomain.CurrentDomain.BaseDirectory;
            CFGFILE = $"{path}{System.IO.Path.GetFileNameWithoutExtension(asb.Location)}.xml";
            tbVerN.Text = $"{asb.GetName().Version} ({vercode})";
            CheckFLan();
            ReadCfg();
            ReadLan();
            cbLan.SelectionChanged += (sender, e) =>
            {
                ReadLan();
                WriteCfg();
            };
            string[] startargs = Environment.GetCommandLineArgs();
            DEBUG = startargs.Length > 1 && startargs[1].ToLower() == "debug";
        }

        private void ReadLan()
        {
            string lanname = cbLan.SelectedItem.ToString();

            CLan.Clear();
            if (FLan.ContainsKey(lanname) && System.IO.File.Exists(FLan[lanname]))
            {
                try
                {
                    XmlDocument doc = new XmlDocument();
                    doc.Load(FLan[lanname]);
                    using (XmlNodeList tabs = doc.SelectNodes("Langue/Item"))
                    {
                        for (int i = 0; i < tabs.Count; i++)
                        {
                            string k = tabs[i].Attributes["from"].Value;
                            string v = tabs[i].Attributes["to"].Value;
                            if (!string.IsNullOrWhiteSpace(k))
                            {
                                CLan.Add(k, v);
                            }
                        }
                    }
                }
                catch (Exception)
                { }
            }

            Title = Trans("中文字體簡繁處理工具");
            p1.Content = Trans("生成簡繁字體");
            p2.Content = Trans("補充字庫");
            p3.Content = tbSet.Text = Trans("設定");
            tbMd.Text = Trans("處理方式");
            rdST.Content = Trans("生成簡轉繁字體");
            rdTS.Content = Trans("生成繁轉簡字體");
            tbIn.Text = Trans("要處理的字體");
            tbOut.Text = Trans("保存爲");
            tbTool.Text = Trans("處理工具");
            ckV.Content = Trans("使用簡繁異體補充字庫");
            tbSTMul.Text = Trans("一簡多繁處理方式");
            rdSTN.Content = Trans("不處理一簡多繁");
            rdSTOne.Content = Trans("使用單一常用字");
            rdSTM.Content = Trans("使用詞彙動態匹配");
            rdSTMT.Content = Trans("使用臺灣詞彙動態匹配");
            tbSTVar.Text = Trans("繁體異體字選擇");
            rdVDef.Content = Trans("預設");
            rdVTW.Content = Trans("臺灣");
            rdVHK.Content = Trans("香港");
            rdVOld.Content = Trans("舊字形");
            ckName.Content = Trans("修改字體名稱");
            tbNE.Text = Trans("* 字體名稱(英)");
            rdMg.Content = Trans("從其他字體補入");
            rdVar.Content = Trans("使用字體本身簡繁異體補充");
            rdFan.Content = Trans("合併簡體與簡入繁出字體");
            tbIn2.Text = Trans("補入的字體");
            tbInT2.Text = Trans("簡入繁出字體");
            tbLan.Text = Trans("界面語言");
            tbPY.Text = "Python " + Trans("路徑");
            tbFF.Text = "Fontforge " + Trans("路徑");
            tbHome.Text = Trans("官方網站");
            btStart.Content = Trans("開始");
            tbAbout.Text = Trans("關於") + Trans("中文字體簡繁處理工具");
            tbFsIn.Text = Trans("字體列表");
            foreach (Button item in new Button[] { btIn, btOut, btInT2, btPY, btFF })
            {
                item.Content = Trans("選擇");
            }
            ListBox_LayoutUpdated(null, null);
        }

        private void ReadCfg()
        {
            if (System.IO.File.Exists(CFGFILE))
            {
                try
                {
                    XmlDocument doc = new XmlDocument();
                    doc.Load(CFGFILE);
                    string lname = doc.SelectSingleNode("Config/Setting/LanName").InnerText;
                    if (cbLan.Items.Contains(lname))
                    {
                        cbLan.SelectedItem = lname;
                    }
                    string pyrd = doc.SelectSingleNode("Config/Setting/PyPath").InnerText;
                    string ffrd = doc.SelectSingleNode("Config/Setting/FFPath").InnerText;
                    if (!string.IsNullOrWhiteSpace(pyrd))
                    {
                        txPY.Text = pyrd;
                    }
                    if (!string.IsNullOrWhiteSpace(ffrd))
                    {
                        txFF.Text = ffrd;
                    }
                }
                catch (Exception)
                {
                    UseSysLan();
                }
            }
            else
            {
                UseSysLan();
            }
        }

        private void UseSysLan()
        {
            string locname = System.Globalization.CultureInfo.CurrentCulture.Name;
            string lanname = "";
            if (locname == "zh-TW")
                lanname = "正體中文";
            else if (locname == "zh-CN" || locname == "zh-SG")
                lanname = "简体中文";
            if (cbLan.Items.Contains(lanname))
                cbLan.SelectedItem = lanname;
        }

        private void WriteCfg()
        {
            XmlDocument doc = new XmlDocument();
            doc.AppendChild(doc.CreateXmlDeclaration("1.0", "utf-8", null));
            doc.AppendChild(doc.CreateElement("Config"));
            doc.SelectSingleNode("Config").AppendChild(doc.CreateElement("Setting"));
            doc.SelectSingleNode("Config/Setting").AppendChild(doc.CreateElement("LanName")).InnerText = cbLan.SelectedItem.ToString();
            doc.SelectSingleNode("Config/Setting").AppendChild(doc.CreateElement("PyPath")).InnerText = txPY.Text;
            doc.SelectSingleNode("Config/Setting").AppendChild(doc.CreateElement("FFPath")).InnerText = txFF.Text;
            doc.Save(CFGFILE);
        }

        private void CheckFLan()
        {
            cbLan.Items.Add("預設(繁體中文)");
            if (System.IO.Directory.Exists($"{path}locales"))
            {
                string[] lanxmls = System.IO.Directory.GetFiles($"{path}locales", "*.xml");
                foreach (string item in lanxmls)
                {
                    try
                    {
                        XmlDocument doc = new XmlDocument();
                        doc.Load(item);
                        string lname = doc.SelectSingleNode("Langue").Attributes["name"].Value;
                        if (!string.IsNullOrWhiteSpace(lname) && !FLan.ContainsKey(lname))
                        {
                            FLan.Add(lname, item);
                        }
                    }
                    catch (Exception)
                    { }
                }
                foreach (string item in FLan.Keys)
                {
                    if (!cbLan.Items.Contains(item))
                    {
                        cbLan.Items.Add(item);
                    }
                }
            }
        }

        private void MainWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (!(thread is null) && thread.IsAlive)
            {
                e.Cancel = true;
            }
        }

        private void DisableElement(object sender, RoutedEventArgs e) => DisableElement();

        private void DisableElement()
        {
            gdST.IsEnabled = rdST.IsChecked == true;
            gdName.IsEnabled = ckName.IsChecked == true;
            btFs.IsEnabled = rdMg.IsChecked == true;
            btInT2.IsEnabled = txInT2.IsEnabled = rdFan.IsChecked == true;
            gdSTVar.IsEnabled = rdSTMT.IsChecked != true;
        }

        private void P_Click(object sender, RoutedEventArgs e)
        {
            foreach (Button bt in ps)
            {
                bt.Style = bt == sender ? (Style)Resources["ButtonHL"] : (Style)Resources["ButtonStyle"];
            }
            tab1.SelectedIndex = sender == p3 ? 1 : 0;
            if (sender == p1)
            {
                ckV.Visibility = Visibility.Visible;
                spMD1.Visibility = Visibility.Visible;
                ckHint.Visibility = Visibility.Collapsed;
                spMD2.Visibility = Visibility.Collapsed;
                bdST.Visibility = Visibility.Visible;
                bdMerge.Visibility = Visibility.Collapsed;
            }
            else if (sender == p2)
            {
                ckV.Visibility = Visibility.Collapsed;
                spMD1.Visibility = Visibility.Collapsed;
                ckHint.Visibility = Visibility.Visible;
                spMD2.Visibility = Visibility.Visible;
                bdMerge.Visibility = Visibility.Visible;
                bdST.Visibility = Visibility.Collapsed;
            }
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e) => DragMove();

        private void BtBack_Click(object sender, RoutedEventArgs e) => tab1.SelectedIndex = 0;

        private void BtFs_Click(object sender, RoutedEventArgs e) => tab1.SelectedIndex = 2;

        private void BtStart_Click(object sender, RoutedEventArgs e)
        {
            string filein = txIn1.Text.Trim();
            string filein2 = txInT2.Text.Trim();
            string fileout = txOut1.Text.Trim();
            bool isST = spMD1.IsVisible == true;
            bool isOtfcc = rdOtfcc.IsChecked == true;
            if ((!System.IO.File.Exists(filein)) || (!System.IO.File.Exists(filein2) && !isST && rdFan.IsChecked == true) || string.IsNullOrWhiteSpace(fileout))
            {
                MessageBox.Show(Trans("文件無效，請重新選擇。"), "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }
            if (!isST && rdMg.IsChecked == true && listBox.Items.Count < 1)
            {
                MessageBox.Show(Trans("請添加補入的字體。"), "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }
            string exefile = SetExec(isOtfcc);
            if (!System.IO.File.Exists(exefile))
            {
                string exename = isOtfcc ? "Python" : "FontForge";
                MessageBox.Show($"未找到 {exename}，" + Trans("請在設定中重新填寫程序路徑。"), "提示", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }
            string pyfile = isOtfcc ? $"{path}converto.py" : $"{path}convertf.py";
            string cmdline = $"\"{pyfile}\" -i \"{filein}\" -o \"{fileout}\"";
            string runmd = "";
            RadioButton[] rdSTs = new RadioButton[] { rdSTN, rdSTOne, rdSTM, rdSTMT };
            RadioButton[] rdVs = new RadioButton[] { rdVDef, rdVTW, rdVHK, rdVOld };
            runmd += isST ? "0" : "1";
            if (isST)
            {
                runmd += rdST.IsChecked == true ? "0" : "1";
                foreach (RadioButton rd in rdSTs)
                {
                    if (rd.IsChecked == true)
                    {
                        runmd += Array.IndexOf(rdSTs, rd).ToString();
                        break;
                    }
                }
                foreach (RadioButton rd in rdVs)
                {
                    if (rd.IsChecked == true)
                    {
                        runmd += Array.IndexOf(rdVs, rd).ToString();
                        break;
                    }
                }
            }
            else
            {
                if (rdMg.IsChecked == true) runmd += "0";
                else if (rdVar.IsChecked == true) runmd += "1";
                else runmd += "2";
            }
            cmdline += $" -wk {runmd}";
            if (isST && ckV.IsChecked == true)
            {
                cmdline += " -v";
            }
            if (ckName.IsChecked == true)
            {
                if (string.IsNullOrWhiteSpace(txNE.Text))
                {
                    MessageBox.Show(Trans("「字體名稱(英)」不能爲空。"), "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }
                else
                {
                    cmdline += $" -n \"{txNE.Text}\"";
                    if (!string.IsNullOrWhiteSpace(txNT.Text))
                    {
                        cmdline += $" -n1 \"{txNT.Text}\"";
                    }
                    if (!string.IsNullOrWhiteSpace(txNS.Text))
                    {
                        cmdline += $" -n2 \"{txNT.Text}\"";
                    }
                    if (!string.IsNullOrWhiteSpace(txNV.Text))
                    {
                        cmdline += $" -n3 \"{txNV.Text}\"";
                    }
                }
            }
            if (!isST)
            {
                if (rdMg.IsChecked == true)
                {
                    foreach (var item in listBox.Items)
                    {
                        cmdline += $" -i2 \"{item}\"";
                    }
                }
                else if (rdFan.IsChecked == true)
                {
                    cmdline += $" -i2 \"{filein2}\"";
                }
                if (ckHint.IsChecked == true)
                {
                    cmdline += " -ih";
                }
            }
            cmdline = $"\"{exefile}\" -u -X utf8 {cmdline}";
            if (!isOtfcc)
            {
                try
                {
                    string ffpath = System.IO.Directory.GetParent(exefile).Parent.FullName;
                    cmdline = $"set \"PYTHONHOME={ffpath}\"&{cmdline}";
                }
                catch (Exception)
                { }
            }

            tab1.SelectedIndex = 3;
            Cursor = Cursors.Wait;
            tbInfo.Text = Trans("正在處理，請稍後...");
            spHead.IsEnabled = false;
            btBack2.IsEnabled = false;
            listBox2.Items.Clear();

            thread = new System.Threading.Thread(() => RunPy(cmdline, fileout));
            thread.IsBackground = true;
            thread.Start();
        }

        private void RunPy(string cmdline, string fileout)
        {
            string errinfo = "";
            string outinfo = "";
            using (System.Diagnostics.Process p = new System.Diagnostics.Process())
            {
                p.StartInfo.StandardOutputEncoding = Encoding.UTF8;
                p.StartInfo.StandardErrorEncoding = Encoding.UTF8;
                p.StartInfo.FileName = "cmd";
                p.StartInfo.Arguments = $"/c \"{cmdline}\"";
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.RedirectStandardError = true;
                p.StartInfo.RedirectStandardOutput = true;
                p.Start();
                p.OutputDataReceived += new DataReceivedEventHandler((object sender, DataReceivedEventArgs e) =>
                {
                    if (!string.IsNullOrWhiteSpace(e.Data))
                    {
                        Dispatcher.Invoke(new Action(delegate
                        {
                            ListBoxItem listBoxItem = new ListBoxItem();
                            listBoxItem.Content = e.Data;
                            listBox2.Items.Add(listBoxItem);
                        }));
                        outinfo = e.Data;
                    }
                });
                p.ErrorDataReceived += new DataReceivedEventHandler((object sender, DataReceivedEventArgs e) =>
                {
                    if (!string.IsNullOrWhiteSpace(e.Data) && (DEBUG || e.Data.Contains("Error") || e.Data.Contains("ERROR") || e.Data.Contains("[Errno")) && !e.Data.Contains("raise"))
                    {
                        Dispatcher.Invoke(new Action(delegate
                        {
                            ListBoxItem listBoxItem = new ListBoxItem();
                            listBoxItem.Content = e.Data;
                            listBoxItem.Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("Red"));
                            listBox2.Items.Add(listBoxItem);
                        }));
                        errinfo += $"{e.Data}\r\n";
                    }
                });
                p.BeginErrorReadLine();
                p.BeginOutputReadLine();
                p.WaitForExit();
                p.Close();
            }
            string outPrint = Trans("程序執行完畢。");
            if (System.IO.File.Exists(fileout))
            {
                if (outinfo.EndsWith("Finished!"))
                {
                    outPrint += string.IsNullOrWhiteSpace(errinfo) ? $"\r\n{Trans("成功！")}" : $"\r\n{Trans("出現錯誤！")}";
                }
                else if (!string.IsNullOrWhiteSpace(errinfo))
                {
                    outPrint += $"\r\n{Trans("失敗！")}";
                }
            }
            else
            {
                outPrint += $"\r\n{Trans("失敗！")}";
            }

            SystemSounds.Beep.Play();
            Dispatcher.Invoke(new Action(delegate
            {
                spHead.IsEnabled = true;
                btBack2.IsEnabled = true;
                tbInfo.Text = outPrint;
                Cursor = Cursors.Arrow;
                IntPtr hwnd = new System.Windows.Interop.WindowInteropHelper(this).Handle;
                FlashWindow(hwnd, true);
            }));
        }

        private string SetExec(bool ispy)
        {
            string[] pths = ispy
                ? (new string[] { txPY.Text, path + txPY.Text, "python/python.exe", path + "python/python.exe" })
                : (new string[] { txFF.Text, path + txFF.Text, "FontForgeBuilds/bin/ffpython.exe", path + "FontForgeBuilds/bin/ffpython.exe", "C:/Program Files (x86)/FontForgeBuilds/bin/ffpython.exe", "C:/Program Files/FontForgeBuilds/bin/ffpython.exe" });
            foreach (string pt in pths)
            {
                if (System.IO.File.Exists(pt))
                {
                    return pt;
                }
            }
            return ispy ? TryEnvironmen("python") : TryEnvironmen("ffpython");
        }

        private string TryEnvironmen(string v)
        {
            foreach (string s in (Environment.GetEnvironmentVariable("PATH") ?? "").Split(';'))
            {
                string evpath = s.Trim();
                if (!string.IsNullOrEmpty(evpath))
                {
                    string[] ckevns = { System.IO.Path.Combine(evpath, v), System.IO.Path.Combine(evpath, v + ".exe"), System.IO.Path.Combine(evpath, v + ".com") };
                    foreach (string ckevn in ckevns)
                    {
                        if (System.IO.File.Exists(ckevn))
                        {
                            return ckevn;
                        }
                    }
                }
            }
            return null;
        }

        private void ListBox_Drop(object sender, DragEventArgs e)
        {
            Array file = (System.Array)e.Data.GetData(DataFormats.FileDrop);
            foreach (var item in file)
            {
                if (System.IO.File.Exists((string)item))
                {
                    listBox.Items.Add((string)item);
                }
            }
        }

        private void ButtonList_Click(object sender, RoutedEventArgs e)
        {
            int i = listBox.SelectedIndex;
            openFileDialog.Filter = $"{Trans("字體文件")}|*.ttf;*.otf|{Trans("所有文件")}|*";
            openFileDialog.Multiselect = true;
            if (sender == btAdd && openFileDialog.ShowDialog() == true)
            {
                foreach (var item in openFileDialog.FileNames)
                {
                    listBox.Items.Add(item);
                }
            }
            else if (sender == btInst && listBox.SelectedIndex > -1 && openFileDialog.ShowDialog() == true)
            {
                foreach (var item in openFileDialog.FileNames)
                {
                    listBox.Items.Insert(listBox.SelectedIndex, item);
                }
            }
            else if (sender == btRmv && i >= 0)
            {
                listBox.Items.RemoveAt(i);
                listBox.SelectedIndex = listBox.Items.Count > i ? i : i - 1;
            }
            else if (sender == btUp && i > 0)
            {
                (listBox.Items[i], listBox.Items[i - 1]) = (listBox.Items[i - 1], listBox.Items[i]);
                listBox.SelectedIndex = i - 1;
            }
            else if (sender == btDn && i >= 0 && i < listBox.Items.Count - 1)
            {
                (listBox.Items[i + 1], listBox.Items[i]) = (listBox.Items[i], listBox.Items[i + 1]);
                listBox.SelectedIndex = i + 1;
            }
            else if (sender == btClr)
            {
                listBox.Items.Clear();
            }
        }

        private string Trans(string v)
        {
            return CLan.ContainsKey(v) && !string.IsNullOrWhiteSpace(CLan[v]) ? CLan[v] : v;
        }

        private void ListBox_LayoutUpdated(object sender, EventArgs e)
        {
            btFs.Content = listBox.Items.Count < 1 ? Trans("點擊添加字體") : $"已添加 {listBox.Items.Count} {Trans("個字體，點擊修改")}";
        }

        private void Choose_Click(object sender, RoutedEventArgs e)
        {
            openFileDialog.Multiselect = false;
            if (sender == btIn)
            {
                openFileDialog.Filter = $"{Trans("字體文件")}|*.ttf;*.otf|{Trans("所有文件")}|*";
                if (openFileDialog.ShowDialog() == true)
                {
                    txIn1.Text = openFileDialog.FileName;
                }
            }
            else if (sender == btOut)
            {
                saveFileDialog.Filter = $"{Trans("字體文件")}|*.ttf;*.otf|{Trans("所有文件")}|*";
                if (saveFileDialog.ShowDialog() == true)
                {
                    txOut1.Text = saveFileDialog.FileName;
                }
            }
            else if (sender == btInT2)
            {
                openFileDialog.Filter = $"{Trans("字體文件")}|*.ttf;*.otf|{Trans("所有文件")}|*";
                if (openFileDialog.ShowDialog() == true)
                {
                    txInT2.Text = openFileDialog.FileName;
                }
            }
            else if (sender == btPY)
            {
                openFileDialog.Filter = $"python|python.exe|{Trans("所有文件")}|*.*";
                if (openFileDialog.ShowDialog() == true)
                {
                    txPY.Text = openFileDialog.FileName;
                }
            }
            else if (sender == btFF)
            {
                openFileDialog.Filter = $"ffpython|ffpython.exe|{Trans("所有文件")}|*.*";
                if (openFileDialog.ShowDialog() == true)
                {
                    txFF.Text = openFileDialog.FileName;
                }
            }
        }

        private void TextBox_PreviewDragOver(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                e.Effects = DragDropEffects.All;
                e.Handled = true;
            }
            else
            {
                e.Effects = DragDropEffects.None;
            }
        }

        private void TextBox_Drop(object sender, DragEventArgs e) => ((TextBox)sender).Text = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();

        private void TextboxPY_LostFocus(object sender, RoutedEventArgs e) => WriteCfg();

        [System.Runtime.InteropServices.DllImport("User32.dll", CharSet = System.Runtime.InteropServices.CharSet.Unicode, EntryPoint = "FlashWindow")]
        private static extern void FlashWindow(IntPtr hwnd, bool bInvert);

        private void Hyperlink_RequestNavigate(object sender, System.Windows.Navigation.RequestNavigateEventArgs e)
        {
            System.Diagnostics.Process.Start(e.Uri.AbsoluteUri);
        }
    }
}
