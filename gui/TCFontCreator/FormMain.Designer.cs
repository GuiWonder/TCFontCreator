namespace TCFontCreator
{
    partial class FormMain
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
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
            this.panelMain = new System.Windows.Forms.Panel();
            this.linkLabel1 = new System.Windows.Forms.LinkLabel();
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
            this.panel1.SuspendLayout();
            this.panelMain.SuspendLayout();
            this.panelTC.SuspendLayout();
            this.SuspendLayout();
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(18, 13);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(53, 12);
            this.label7.TabIndex = 5;
            this.label7.Text = "選擇目標";
            // 
            // comboBoxSys
            // 
            this.comboBoxSys.BackColor = System.Drawing.SystemColors.Window;
            this.comboBoxSys.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxSys.FormattingEnabled = true;
            this.comboBoxSys.Items.AddRange(new object[] {
            "生成簡轉繁字體",
            "使用同義字補全字庫",
            "合併簡體 GB2312、繁體 GB2312",
            "合併字體1、字體2",
            "日本字體新字形轉爲舊字形(僅部分字體)",
            "生成繁轉簡字體"});
            this.comboBoxSys.Location = new System.Drawing.Point(77, 9);
            this.comboBoxSys.Name = "comboBoxSys";
            this.comboBoxSys.Size = new System.Drawing.Size(292, 20);
            this.comboBoxSys.TabIndex = 0;
            this.comboBoxSys.SelectedIndexChanged += new System.EventHandler(this.ComboBoxSys_SelectedIndexChanged);
            // 
            // buttonStart
            // 
            this.buttonStart.Location = new System.Drawing.Point(392, 7);
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
            this.labeli1.Location = new System.Drawing.Point(6, 46);
            this.labeli1.Name = "labeli1";
            this.labeli1.Size = new System.Drawing.Size(71, 12);
            this.labeli1.TabIndex = 1;
            this.labeli1.Text = "* 輸入字體1";
            // 
            // labelo
            // 
            this.labelo.AutoSize = true;
            this.labelo.Location = new System.Drawing.Point(11, 94);
            this.labelo.Name = "labelo";
            this.labelo.Size = new System.Drawing.Size(65, 12);
            this.labelo.TabIndex = 2;
            this.labelo.Text = "* 輸出字體";
            // 
            // textBoxIn
            // 
            this.textBoxIn.AllowDrop = true;
            this.textBoxIn.Location = new System.Drawing.Point(77, 43);
            this.textBoxIn.Name = "textBoxIn";
            this.textBoxIn.Size = new System.Drawing.Size(353, 21);
            this.textBoxIn.TabIndex = 1;
            this.textBoxIn.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxIn.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // textBoxOut
            // 
            this.textBoxOut.AllowDrop = true;
            this.textBoxOut.Location = new System.Drawing.Point(77, 91);
            this.textBoxOut.Name = "textBoxOut";
            this.textBoxOut.Size = new System.Drawing.Size(353, 21);
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
            this.checkBoxInfo.Location = new System.Drawing.Point(19, 217);
            this.checkBoxInfo.Name = "checkBoxInfo";
            this.checkBoxInfo.Size = new System.Drawing.Size(102, 16);
            this.checkBoxInfo.TabIndex = 5;
            this.checkBoxInfo.Text = "更新字體信息:";
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
            this.label3.Location = new System.Drawing.Point(28, 5);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(65, 12);
            this.label3.TabIndex = 1;
            this.label3.Text = "* 字體名稱";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(18, 125);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(53, 12);
            this.label8.TabIndex = 14;
            this.label8.Text = "使用內核";
            // 
            // comboBoxApp
            // 
            this.comboBoxApp.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxApp.FormattingEnabled = true;
            this.comboBoxApp.Items.AddRange(new object[] {
            "otfcc",
            "FontForge"});
            this.comboBoxApp.Location = new System.Drawing.Point(77, 122);
            this.comboBoxApp.Name = "comboBoxApp";
            this.comboBoxApp.Size = new System.Drawing.Size(156, 20);
            this.comboBoxApp.TabIndex = 13;
            // 
            // checkBoxYitizi
            // 
            this.checkBoxYitizi.AutoSize = true;
            this.checkBoxYitizi.Checked = true;
            this.checkBoxYitizi.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxYitizi.Location = new System.Drawing.Point(253, 124);
            this.checkBoxYitizi.Name = "checkBoxYitizi";
            this.checkBoxYitizi.Size = new System.Drawing.Size(156, 16);
            this.checkBoxYitizi.TabIndex = 10;
            this.checkBoxYitizi.Text = "同時完成同義字補全字庫";
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
            this.panel1.Location = new System.Drawing.Point(110, 215);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(246, 105);
            this.panel1.TabIndex = 17;
            // 
            // panelMain
            // 
            this.panelMain.Controls.Add(this.linkLabel1);
            this.panelMain.Controls.Add(this.panelTC);
            this.panelMain.Controls.Add(this.linkLabelOut);
            this.panelMain.Controls.Add(this.linkLabelIn2);
            this.panelMain.Controls.Add(this.linkLabelIn);
            this.panelMain.Controls.Add(this.label7);
            this.panelMain.Controls.Add(this.panel1);
            this.panelMain.Controls.Add(this.checkBoxInfo);
            this.panelMain.Controls.Add(this.comboBoxSys);
            this.panelMain.Controls.Add(this.checkBoxYitizi);
            this.panelMain.Controls.Add(this.buttonStart);
            this.panelMain.Controls.Add(this.label8);
            this.panelMain.Controls.Add(this.textBoxOut);
            this.panelMain.Controls.Add(this.comboBoxApp);
            this.panelMain.Controls.Add(this.labeli2);
            this.panelMain.Controls.Add(this.labeli1);
            this.panelMain.Controls.Add(this.textBoxIn2);
            this.panelMain.Controls.Add(this.textBoxIn);
            this.panelMain.Controls.Add(this.labelo);
            this.panelMain.Location = new System.Drawing.Point(13, 13);
            this.panelMain.Name = "panelMain";
            this.panelMain.Size = new System.Drawing.Size(478, 327);
            this.panelMain.TabIndex = 18;
            // 
            // linkLabel1
            // 
            this.linkLabel1.AutoSize = true;
            this.linkLabel1.Location = new System.Drawing.Point(11, 307);
            this.linkLabel1.Name = "linkLabel1";
            this.linkLabel1.Size = new System.Drawing.Size(53, 12);
            this.linkLabel1.TabIndex = 22;
            this.linkLabel1.TabStop = true;
            this.linkLabel1.Text = "項目主頁";
            this.linkLabel1.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabel1_LinkClicked);
            // 
            // panelTC
            // 
            this.panelTC.Controls.Add(this.label1);
            this.panelTC.Controls.Add(this.comboBoxVar);
            this.panelTC.Controls.Add(this.labelMilti);
            this.panelTC.Controls.Add(this.comboBoxMulti);
            this.panelTC.Location = new System.Drawing.Point(13, 148);
            this.panelTC.Name = "panelTC";
            this.panelTC.Size = new System.Drawing.Size(417, 63);
            this.panelTC.TabIndex = 21;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(5, 7);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(113, 12);
            this.label1.TabIndex = 19;
            this.label1.Text = "選擇要使用的異體字";
            // 
            // comboBoxVar
            // 
            this.comboBoxVar.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxVar.FormattingEnabled = true;
            this.comboBoxVar.Items.AddRange(new object[] {
            "默認",
            "臺灣",
            "香港",
            "舊字形"});
            this.comboBoxVar.Location = new System.Drawing.Point(125, 3);
            this.comboBoxVar.Name = "comboBoxVar";
            this.comboBoxVar.Size = new System.Drawing.Size(205, 20);
            this.comboBoxVar.TabIndex = 20;
            // 
            // labelMilti
            // 
            this.labelMilti.AutoSize = true;
            this.labelMilti.Location = new System.Drawing.Point(4, 37);
            this.labelMilti.Name = "labelMilti";
            this.labelMilti.Size = new System.Drawing.Size(113, 12);
            this.labelMilti.TabIndex = 19;
            this.labelMilti.Text = "對簡繁一對多的處理";
            // 
            // comboBoxMulti
            // 
            this.comboBoxMulti.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxMulti.FormattingEnabled = true;
            this.comboBoxMulti.Items.AddRange(new object[] {
            "不處理一對多",
            "使用單一常用字",
            "使用詞彙正確一簡對多繁"});
            this.comboBoxMulti.Location = new System.Drawing.Point(125, 33);
            this.comboBoxMulti.Name = "comboBoxMulti";
            this.comboBoxMulti.Size = new System.Drawing.Size(205, 20);
            this.comboBoxMulti.TabIndex = 20;
            // 
            // linkLabelOut
            // 
            this.linkLabelOut.AutoSize = true;
            this.linkLabelOut.Location = new System.Drawing.Point(436, 94);
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
            this.linkLabelIn2.Location = new System.Drawing.Point(436, 70);
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
            this.linkLabelIn.Location = new System.Drawing.Point(436, 46);
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
            this.labeli2.Location = new System.Drawing.Point(6, 70);
            this.labeli2.Name = "labeli2";
            this.labeli2.Size = new System.Drawing.Size(71, 12);
            this.labeli2.TabIndex = 1;
            this.labeli2.Text = "* 輸入字體2";
            // 
            // textBoxIn2
            // 
            this.textBoxIn2.AllowDrop = true;
            this.textBoxIn2.Location = new System.Drawing.Point(77, 67);
            this.textBoxIn2.Name = "textBoxIn2";
            this.textBoxIn2.Size = new System.Drawing.Size(353, 21);
            this.textBoxIn2.TabIndex = 1;
            this.textBoxIn2.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxIn2.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // FormMain
            // 
            this.AcceptButton = this.buttonStart;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(506, 344);
            this.Controls.Add(this.panelMain);
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
            this.panelMain.ResumeLayout(false);
            this.panelMain.PerformLayout();
            this.panelTC.ResumeLayout(false);
            this.panelTC.PerformLayout();
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
        private System.Windows.Forms.Panel panelMain;
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
        private System.Windows.Forms.LinkLabel linkLabel1;
    }
}

