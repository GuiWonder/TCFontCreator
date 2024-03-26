namespace TCFontCreator
{
    partial class FormMain
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label7 = new System.Windows.Forms.Label();
            this.comboBoxSys = new System.Windows.Forms.ComboBox();
            this.buttonStart = new System.Windows.Forms.Button();
            this.labeli1 = new System.Windows.Forms.Label();
            this.labelo = new System.Windows.Forms.Label();
            this.textBoxIn = new System.Windows.Forms.TextBox();
            this.textBoxOut = new System.Windows.Forms.TextBox();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.checkBoxInfo = new System.Windows.Forms.CheckBox();
            this.label5 = new System.Windows.Forms.Label();
            this.textBoxName = new System.Windows.Forms.TextBox();
            this.textBoxVersi = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.textBoxTCName = new System.Windows.Forms.TextBox();
            this.textBoxSCName = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.comboBoxApp = new System.Windows.Forms.ComboBox();
            this.checkBoxYitizi = new System.Windows.Forms.CheckBox();
            this.panel1 = new System.Windows.Forms.Panel();
            this.panelTC = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.comboBoxVar = new System.Windows.Forms.ComboBox();
            this.labelMilti = new System.Windows.Forms.Label();
            this.comboBoxMulti = new System.Windows.Forms.ComboBox();
            this.linkLabelOut = new System.Windows.Forms.LinkLabel();
            this.linkLabelIn2 = new System.Windows.Forms.LinkLabel();
            this.linkLabelIn = new System.Windows.Forms.LinkLabel();
            this.labeli2 = new System.Windows.Forms.Label();
            this.textBoxIn2 = new System.Windows.Forms.TextBox();
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.comboBoxMg = new System.Windows.Forms.ComboBox();
            this.buttonFontsList = new System.Windows.Forms.Button();
            this.label10 = new System.Windows.Forms.Label();
            this.tabPage3 = new System.Windows.Forms.TabPage();
            this.linkLabel1 = new System.Windows.Forms.LinkLabel();
            this.linkLabelFF = new System.Windows.Forms.LinkLabel();
            this.linkLabelPy = new System.Windows.Forms.LinkLabel();
            this.label14 = new System.Windows.Forms.Label();
            this.label12 = new System.Windows.Forms.Label();
            this.comboBoxLan = new System.Windows.Forms.ComboBox();
            this.label13 = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.textBoxFFPth = new System.Windows.Forms.TextBox();
            this.textBoxPypth = new System.Windows.Forms.TextBox();
            this.checkBoxIH = new System.Windows.Forms.CheckBox();
            this.panel1.SuspendLayout();
            this.panelTC.SuspendLayout();
            this.tabControl1.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.tabPage3.SuspendLayout();
            this.SuspendLayout();
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(28, 21);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(53, 12);
            this.label7.TabIndex = 5;
            this.label7.Text = "處理方式";
            // 
            // comboBoxSys
            // 
            this.comboBoxSys.BackColor = System.Drawing.SystemColors.Window;
            this.comboBoxSys.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxSys.FormattingEnabled = true;
            this.comboBoxSys.Items.AddRange(new object[] {
            "生成簡轉繁字體",
            "生成繁轉簡字體"});
            this.comboBoxSys.Location = new System.Drawing.Point(89, 18);
            this.comboBoxSys.Name = "comboBoxSys";
            this.comboBoxSys.Size = new System.Drawing.Size(279, 20);
            this.comboBoxSys.TabIndex = 0;
            this.comboBoxSys.SelectedIndexChanged += new System.EventHandler(this.ComboBoxSys_SelectedIndexChanged);
            // 
            // buttonStart
            // 
            this.buttonStart.Location = new System.Drawing.Point(391, 16);
            this.buttonStart.Name = "buttonStart";
            this.buttonStart.Size = new System.Drawing.Size(75, 23);
            this.buttonStart.TabIndex = 11;
            this.buttonStart.Text = "開始";
            this.buttonStart.UseVisualStyleBackColor = true;
            this.buttonStart.Click += new System.EventHandler(this.ButtonStart_Click);
            // 
            // labeli1
            // 
            this.labeli1.AutoSize = true;
            this.labeli1.Location = new System.Drawing.Point(5, 48);
            this.labeli1.Name = "labeli1";
            this.labeli1.Size = new System.Drawing.Size(77, 12);
            this.labeli1.TabIndex = 1;
            this.labeli1.Text = "要處理的字體";
            // 
            // labelo
            // 
            this.labelo.AutoSize = true;
            this.labelo.Location = new System.Drawing.Point(40, 75);
            this.labelo.Name = "labelo";
            this.labelo.Size = new System.Drawing.Size(41, 12);
            this.labelo.TabIndex = 2;
            this.labelo.Text = "保存爲";
            // 
            // textBoxIn
            // 
            this.textBoxIn.AllowDrop = true;
            this.textBoxIn.Location = new System.Drawing.Point(89, 45);
            this.textBoxIn.Name = "textBoxIn";
            this.textBoxIn.Size = new System.Drawing.Size(341, 21);
            this.textBoxIn.TabIndex = 1;
            this.textBoxIn.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxIn.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // textBoxOut
            // 
            this.textBoxOut.AllowDrop = true;
            this.textBoxOut.Location = new System.Drawing.Point(89, 72);
            this.textBoxOut.Name = "textBoxOut";
            this.textBoxOut.Size = new System.Drawing.Size(341, 21);
            this.textBoxOut.TabIndex = 3;
            this.textBoxOut.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxOut.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.Filter = "字體文件|*.ttf;*.otf|所有文件|*.*";
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.Filter = "字體文件|*.ttf;*.otf|所有文件|*.*";
            // 
            // checkBoxInfo
            // 
            this.checkBoxInfo.AutoSize = true;
            this.checkBoxInfo.Location = new System.Drawing.Point(25, 11);
            this.checkBoxInfo.Name = "checkBoxInfo";
            this.checkBoxInfo.Size = new System.Drawing.Size(102, 16);
            this.checkBoxInfo.TabIndex = 5;
            this.checkBoxInfo.Text = "修改字體名稱:";
            this.checkBoxInfo.UseVisualStyleBackColor = true;
            this.checkBoxInfo.CheckedChanged += new System.EventHandler(this.CheckBoxInfo_CheckedChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(16, 59);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(77, 12);
            this.label5.TabIndex = 1;
            this.label5.Text = "中文名称(简)";
            // 
            // textBoxName
            // 
            this.textBoxName.Location = new System.Drawing.Point(99, 2);
            this.textBoxName.Name = "textBoxName";
            this.textBoxName.Size = new System.Drawing.Size(133, 21);
            this.textBoxName.TabIndex = 6;
            this.textBoxName.Text = "My New Font";
            // 
            // textBoxVersi
            // 
            this.textBoxVersi.Location = new System.Drawing.Point(99, 83);
            this.textBoxVersi.Name = "textBoxVersi";
            this.textBoxVersi.Size = new System.Drawing.Size(133, 21);
            this.textBoxVersi.TabIndex = 9;
            this.textBoxVersi.Text = "1.00";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(16, 32);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(77, 12);
            this.label4.TabIndex = 1;
            this.label4.Text = "中文名稱(繁)";
            // 
            // textBoxTCName
            // 
            this.textBoxTCName.Location = new System.Drawing.Point(99, 29);
            this.textBoxTCName.Name = "textBoxTCName";
            this.textBoxTCName.Size = new System.Drawing.Size(133, 21);
            this.textBoxTCName.TabIndex = 7;
            this.textBoxTCName.Text = "我的新字體";
            // 
            // textBoxSCName
            // 
            this.textBoxSCName.Location = new System.Drawing.Point(99, 56);
            this.textBoxSCName.Name = "textBoxSCName";
            this.textBoxSCName.Size = new System.Drawing.Size(133, 21);
            this.textBoxSCName.TabIndex = 8;
            this.textBoxSCName.Text = "我的新字体";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(64, 86);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(29, 12);
            this.label6.TabIndex = 1;
            this.label6.Text = "版本";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(4, 5);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(89, 12);
            this.label3.TabIndex = 1;
            this.label3.Text = "* 字體名稱(英)";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(28, 105);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(53, 12);
            this.label8.TabIndex = 14;
            this.label8.Text = "處理工具";
            // 
            // comboBoxApp
            // 
            this.comboBoxApp.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxApp.FormattingEnabled = true;
            this.comboBoxApp.Items.AddRange(new object[] {
            "otfcc",
            "FontForge"});
            this.comboBoxApp.Location = new System.Drawing.Point(89, 103);
            this.comboBoxApp.Name = "comboBoxApp";
            this.comboBoxApp.Size = new System.Drawing.Size(156, 20);
            this.comboBoxApp.TabIndex = 13;
            // 
            // checkBoxYitizi
            // 
            this.checkBoxYitizi.AutoSize = true;
            this.checkBoxYitizi.Checked = true;
            this.checkBoxYitizi.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxYitizi.Location = new System.Drawing.Point(275, 105);
            this.checkBoxYitizi.Name = "checkBoxYitizi";
            this.checkBoxYitizi.Size = new System.Drawing.Size(144, 16);
            this.checkBoxYitizi.TabIndex = 10;
            this.checkBoxYitizi.Text = "使用簡繁異體補充字庫";
            this.checkBoxYitizi.UseVisualStyleBackColor = true;
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.label5);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.textBoxName);
            this.panel1.Controls.Add(this.label6);
            this.panel1.Controls.Add(this.textBoxVersi);
            this.panel1.Controls.Add(this.textBoxSCName);
            this.panel1.Controls.Add(this.label4);
            this.panel1.Controls.Add(this.textBoxTCName);
            this.panel1.Location = new System.Drawing.Point(128, 10);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(246, 105);
            this.panel1.TabIndex = 17;
            // 
            // panelTC
            // 
            this.panelTC.Controls.Add(this.label1);
            this.panelTC.Controls.Add(this.comboBoxVar);
            this.panelTC.Controls.Add(this.labelMilti);
            this.panelTC.Controls.Add(this.comboBoxMulti);
            this.panelTC.Location = new System.Drawing.Point(40, 148);
            this.panelTC.Name = "panelTC";
            this.panelTC.Size = new System.Drawing.Size(417, 63);
            this.panelTC.TabIndex = 21;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(22, 35);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(89, 12);
            this.label1.TabIndex = 19;
            this.label1.Text = "繁體異體字選擇";
            // 
            // comboBoxVar
            // 
            this.comboBoxVar.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxVar.FormattingEnabled = true;
            this.comboBoxVar.Items.AddRange(new object[] {
            "預設",
            "臺灣",
            "香港",
            "舊字形"});
            this.comboBoxVar.Location = new System.Drawing.Point(130, 32);
            this.comboBoxVar.Name = "comboBoxVar";
            this.comboBoxVar.Size = new System.Drawing.Size(205, 20);
            this.comboBoxVar.TabIndex = 20;
            // 
            // labelMilti
            // 
            this.labelMilti.AutoSize = true;
            this.labelMilti.Location = new System.Drawing.Point(10, 10);
            this.labelMilti.Name = "labelMilti";
            this.labelMilti.Size = new System.Drawing.Size(101, 12);
            this.labelMilti.TabIndex = 19;
            this.labelMilti.Text = "一簡多繁處理方式";
            // 
            // comboBoxMulti
            // 
            this.comboBoxMulti.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxMulti.FormattingEnabled = true;
            this.comboBoxMulti.Items.AddRange(new object[] {
            "不處理一簡多繁",
            "使用單一常用字",
            "使用詞彙動態匹配",
            "使用臺灣詞彙動態匹配"});
            this.comboBoxMulti.Location = new System.Drawing.Point(131, 6);
            this.comboBoxMulti.Name = "comboBoxMulti";
            this.comboBoxMulti.Size = new System.Drawing.Size(205, 20);
            this.comboBoxMulti.TabIndex = 20;
            // 
            // linkLabelOut
            // 
            this.linkLabelOut.AutoSize = true;
            this.linkLabelOut.Location = new System.Drawing.Point(436, 75);
            this.linkLabelOut.Name = "linkLabelOut";
            this.linkLabelOut.Size = new System.Drawing.Size(29, 12);
            this.linkLabelOut.TabIndex = 18;
            this.linkLabelOut.TabStop = true;
            this.linkLabelOut.Text = "選擇";
            this.linkLabelOut.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabelOut_LinkClicked);
            // 
            // linkLabelIn2
            // 
            this.linkLabelIn2.AutoSize = true;
            this.linkLabelIn2.Location = new System.Drawing.Point(446, 183);
            this.linkLabelIn2.Name = "linkLabelIn2";
            this.linkLabelIn2.Size = new System.Drawing.Size(29, 12);
            this.linkLabelIn2.TabIndex = 18;
            this.linkLabelIn2.TabStop = true;
            this.linkLabelIn2.Text = "選擇";
            this.linkLabelIn2.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabelIn2_LinkClicked);
            // 
            // linkLabelIn
            // 
            this.linkLabelIn.AutoSize = true;
            this.linkLabelIn.Location = new System.Drawing.Point(436, 48);
            this.linkLabelIn.Name = "linkLabelIn";
            this.linkLabelIn.Size = new System.Drawing.Size(29, 12);
            this.linkLabelIn.TabIndex = 18;
            this.linkLabelIn.TabStop = true;
            this.linkLabelIn.Text = "選擇";
            this.linkLabelIn.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabelIn_LinkClicked);
            // 
            // labeli2
            // 
            this.labeli2.AutoSize = true;
            this.labeli2.Location = new System.Drawing.Point(32, 183);
            this.labeli2.Name = "labeli2";
            this.labeli2.Size = new System.Drawing.Size(77, 12);
            this.labeli2.TabIndex = 1;
            this.labeli2.Text = "簡入繁出字體";
            // 
            // textBoxIn2
            // 
            this.textBoxIn2.AllowDrop = true;
            this.textBoxIn2.Location = new System.Drawing.Point(115, 180);
            this.textBoxIn2.Name = "textBoxIn2";
            this.textBoxIn2.Size = new System.Drawing.Size(325, 21);
            this.textBoxIn2.TabIndex = 1;
            this.textBoxIn2.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxIn2.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Controls.Add(this.tabPage3);
            this.tabControl1.Location = new System.Drawing.Point(12, 12);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(492, 368);
            this.tabControl1.TabIndex = 19;
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.groupBox3);
            this.tabPage1.Controls.Add(this.groupBox1);
            this.tabPage1.Controls.Add(this.panelTC);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(484, 342);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "生成簡繁字體";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.checkBoxInfo);
            this.groupBox3.Controls.Add(this.panel1);
            this.groupBox3.Location = new System.Drawing.Point(10, 217);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(471, 121);
            this.groupBox3.TabIndex = 24;
            this.groupBox3.TabStop = false;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.comboBoxSys);
            this.groupBox1.Controls.Add(this.label7);
            this.groupBox1.Controls.Add(this.labeli1);
            this.groupBox1.Controls.Add(this.labelo);
            this.groupBox1.Controls.Add(this.checkBoxYitizi);
            this.groupBox1.Controls.Add(this.textBoxIn);
            this.groupBox1.Controls.Add(this.textBoxOut);
            this.groupBox1.Controls.Add(this.linkLabelIn);
            this.groupBox1.Controls.Add(this.linkLabelOut);
            this.groupBox1.Controls.Add(this.buttonStart);
            this.groupBox1.Controls.Add(this.label8);
            this.groupBox1.Controls.Add(this.comboBoxApp);
            this.groupBox1.Location = new System.Drawing.Point(10, 6);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(471, 136);
            this.groupBox1.TabIndex = 23;
            this.groupBox1.TabStop = false;
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.groupBox4);
            this.tabPage2.Controls.Add(this.groupBox2);
            this.tabPage2.Controls.Add(this.buttonFontsList);
            this.tabPage2.Controls.Add(this.label10);
            this.tabPage2.Controls.Add(this.labeli2);
            this.tabPage2.Controls.Add(this.linkLabelIn2);
            this.tabPage2.Controls.Add(this.textBoxIn2);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(484, 342);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "補充字庫";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // groupBox4
            // 
            this.groupBox4.Location = new System.Drawing.Point(10, 217);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(471, 121);
            this.groupBox4.TabIndex = 26;
            this.groupBox4.TabStop = false;
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.checkBoxIH);
            this.groupBox2.Controls.Add(this.comboBoxMg);
            this.groupBox2.Location = new System.Drawing.Point(10, 6);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(471, 136);
            this.groupBox2.TabIndex = 25;
            this.groupBox2.TabStop = false;
            // 
            // comboBoxMg
            // 
            this.comboBoxMg.BackColor = System.Drawing.SystemColors.Window;
            this.comboBoxMg.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxMg.FormattingEnabled = true;
            this.comboBoxMg.Items.AddRange(new object[] {
            "從其他字體補入",
            "使用字體本身簡繁異體補充",
            "合併簡體與簡入繁出字體"});
            this.comboBoxMg.Location = new System.Drawing.Point(89, 18);
            this.comboBoxMg.Name = "comboBoxMg";
            this.comboBoxMg.Size = new System.Drawing.Size(279, 20);
            this.comboBoxMg.TabIndex = 19;
            // 
            // buttonFontsList
            // 
            this.buttonFontsList.Location = new System.Drawing.Point(115, 153);
            this.buttonFontsList.Name = "buttonFontsList";
            this.buttonFontsList.Size = new System.Drawing.Size(196, 23);
            this.buttonFontsList.TabIndex = 23;
            this.buttonFontsList.Text = "點擊添加字體";
            this.buttonFontsList.UseVisualStyleBackColor = true;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(42, 158);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(65, 12);
            this.label10.TabIndex = 1;
            this.label10.Text = "補入的字體";
            // 
            // tabPage3
            // 
            this.tabPage3.Controls.Add(this.linkLabel1);
            this.tabPage3.Controls.Add(this.linkLabelFF);
            this.tabPage3.Controls.Add(this.linkLabelPy);
            this.tabPage3.Controls.Add(this.label14);
            this.tabPage3.Controls.Add(this.label12);
            this.tabPage3.Controls.Add(this.comboBoxLan);
            this.tabPage3.Controls.Add(this.label13);
            this.tabPage3.Controls.Add(this.label11);
            this.tabPage3.Controls.Add(this.textBoxFFPth);
            this.tabPage3.Controls.Add(this.textBoxPypth);
            this.tabPage3.Location = new System.Drawing.Point(4, 22);
            this.tabPage3.Name = "tabPage3";
            this.tabPage3.Size = new System.Drawing.Size(484, 342);
            this.tabPage3.TabIndex = 2;
            this.tabPage3.Text = "設定";
            this.tabPage3.UseVisualStyleBackColor = true;
            // 
            // linkLabel1
            // 
            this.linkLabel1.AutoSize = true;
            this.linkLabel1.Location = new System.Drawing.Point(97, 145);
            this.linkLabel1.Name = "linkLabel1";
            this.linkLabel1.Size = new System.Drawing.Size(257, 12);
            this.linkLabel1.TabIndex = 22;
            this.linkLabel1.TabStop = true;
            this.linkLabel1.Text = "https://github.com/GuiWonder/TCFontCreator";
            this.linkLabel1.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabel1_LinkClicked);
            // 
            // linkLabelFF
            // 
            this.linkLabelFF.AutoSize = true;
            this.linkLabelFF.Location = new System.Drawing.Point(445, 99);
            this.linkLabelFF.Name = "linkLabelFF";
            this.linkLabelFF.Size = new System.Drawing.Size(29, 12);
            this.linkLabelFF.TabIndex = 19;
            this.linkLabelFF.TabStop = true;
            this.linkLabelFF.Text = "選擇";
            // 
            // linkLabelPy
            // 
            this.linkLabelPy.AutoSize = true;
            this.linkLabelPy.Location = new System.Drawing.Point(445, 63);
            this.linkLabelPy.Name = "linkLabelPy";
            this.linkLabelPy.Size = new System.Drawing.Size(29, 12);
            this.linkLabelPy.TabIndex = 19;
            this.linkLabelPy.TabStop = true;
            this.linkLabelPy.Text = "選擇";
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(38, 145);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(53, 12);
            this.label14.TabIndex = 7;
            this.label14.Text = "官方網站";
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(38, 27);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(53, 12);
            this.label12.TabIndex = 7;
            this.label12.Text = "界面語言";
            // 
            // comboBoxLan
            // 
            this.comboBoxLan.BackColor = System.Drawing.SystemColors.Window;
            this.comboBoxLan.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxLan.FormattingEnabled = true;
            this.comboBoxLan.Items.AddRange(new object[] {
            "預設繁體中文",
            "简体中文",
            "繁體中文臺灣"});
            this.comboBoxLan.Location = new System.Drawing.Point(99, 24);
            this.comboBoxLan.Name = "comboBoxLan";
            this.comboBoxLan.Size = new System.Drawing.Size(279, 20);
            this.comboBoxLan.TabIndex = 6;
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(2, 99);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(89, 12);
            this.label13.TabIndex = 2;
            this.label13.Text = "Fontforge 路徑";
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(20, 60);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(71, 12);
            this.label11.TabIndex = 2;
            this.label11.Text = "Python 路徑";
            // 
            // textBoxFFPth
            // 
            this.textBoxFFPth.AllowDrop = true;
            this.textBoxFFPth.Location = new System.Drawing.Point(99, 96);
            this.textBoxFFPth.Name = "textBoxFFPth";
            this.textBoxFFPth.Size = new System.Drawing.Size(340, 21);
            this.textBoxFFPth.TabIndex = 3;
            this.textBoxFFPth.Text = "FontForgeBuilds\\bin\\ffpython.exe";
            // 
            // textBoxPypth
            // 
            this.textBoxPypth.AllowDrop = true;
            this.textBoxPypth.Location = new System.Drawing.Point(99, 60);
            this.textBoxPypth.Name = "textBoxPypth";
            this.textBoxPypth.Size = new System.Drawing.Size(340, 21);
            this.textBoxPypth.TabIndex = 3;
            this.textBoxPypth.Text = "python\\python.exe";
            // 
            // checkBoxIH
            // 
            this.checkBoxIH.AutoSize = true;
            this.checkBoxIH.Location = new System.Drawing.Point(275, 105);
            this.checkBoxIH.Name = "checkBoxIH";
            this.checkBoxIH.Size = new System.Drawing.Size(96, 16);
            this.checkBoxIH.TabIndex = 20;
            this.checkBoxIH.Text = "移除 hinting";
            this.checkBoxIH.UseVisualStyleBackColor = true;
            // 
            // FormMain
            // 
            this.AcceptButton = this.buttonStart;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(516, 391);
            this.Controls.Add(this.tabControl1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "FormMain";
            this.ShowIcon = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = " 中文字體簡繁處理工具";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FormMain_FormClosing);
            this.Load += new System.EventHandler(this.FormMain_Load);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.panelTC.ResumeLayout(false);
            this.panelTC.PerformLayout();
            this.tabControl1.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.tabPage2.ResumeLayout(false);
            this.tabPage2.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.tabPage3.ResumeLayout(false);
            this.tabPage3.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Label labeli1;
        private System.Windows.Forms.Label labelo;
        private System.Windows.Forms.TextBox textBoxIn;
        private System.Windows.Forms.TextBox textBoxOut;
        private System.Windows.Forms.Button buttonStart;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.ComboBox comboBoxSys;
        private System.Windows.Forms.CheckBox checkBoxInfo;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox textBoxSCName;
        private System.Windows.Forms.TextBox textBoxTCName;
        private System.Windows.Forms.TextBox textBoxName;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox textBoxVersi;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.CheckBox checkBoxYitizi;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.ComboBox comboBoxApp;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.LinkLabel linkLabelOut;
        private System.Windows.Forms.LinkLabel linkLabelIn;
        private System.Windows.Forms.ComboBox comboBoxMulti;
        private System.Windows.Forms.Label labelMilti;
        private System.Windows.Forms.LinkLabel linkLabelIn2;
        private System.Windows.Forms.Label labeli2;
        private System.Windows.Forms.TextBox textBoxIn2;
        private System.Windows.Forms.Panel panelTC;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox comboBoxVar;
        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.ComboBox comboBoxMg;
        private System.Windows.Forms.TabPage tabPage3;
        private System.Windows.Forms.LinkLabel linkLabel1;
        private System.Windows.Forms.Button buttonFontsList;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.LinkLabel linkLabelFF;
        private System.Windows.Forms.LinkLabel linkLabelPy;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.ComboBox comboBoxLan;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.TextBox textBoxFFPth;
        private System.Windows.Forms.TextBox textBoxPypth;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.CheckBox checkBoxIH;
    }
}

