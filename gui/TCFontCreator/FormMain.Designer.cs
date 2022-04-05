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
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.textBoxIn = new System.Windows.Forms.TextBox();
            this.textBoxOut = new System.Windows.Forms.TextBox();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.checkBoxInfo = new System.Windows.Forms.CheckBox();
            this.label5 = new System.Windows.Forms.Label();
            this.textBoxName = new System.Windows.Forms.TextBox();
            this.textBoxVersi = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.textBoxChName = new System.Windows.Forms.TextBox();
            this.textBoxPSName = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.comboBoxApp = new System.Windows.Forms.ComboBox();
            this.checkBoxYitizi = new System.Windows.Forms.CheckBox();
            this.panel1 = new System.Windows.Forms.Panel();
            this.panelMain = new System.Windows.Forms.Panel();
            this.comboBoxMulti = new System.Windows.Forms.ComboBox();
            this.labelMilti = new System.Windows.Forms.Label();
            this.linkLabelOut = new System.Windows.Forms.LinkLabel();
            this.linkLabelIn = new System.Windows.Forms.LinkLabel();
            this.panel1.SuspendLayout();
            this.panelMain.SuspendLayout();
            this.SuspendLayout();
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(18, 14);
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
            "生成繁體",
            "生成繁體TW",
            "生成繁體HK",
            "生成繁體舊字形",
            "補全同義字"});
            this.comboBoxSys.Location = new System.Drawing.Point(77, 9);
            this.comboBoxSys.Name = "comboBoxSys";
            this.comboBoxSys.Size = new System.Drawing.Size(292, 20);
            this.comboBoxSys.TabIndex = 0;
            this.comboBoxSys.SelectedIndexChanged += new System.EventHandler(this.ComboBoxSys_SelectedIndexChanged);
            // 
            // buttonStart
            // 
            this.buttonStart.Location = new System.Drawing.Point(377, 8);
            this.buttonStart.Name = "buttonStart";
            this.buttonStart.Size = new System.Drawing.Size(75, 23);
            this.buttonStart.TabIndex = 11;
            this.buttonStart.Text = "開始";
            this.buttonStart.UseVisualStyleBackColor = true;
            this.buttonStart.Click += new System.EventHandler(this.ButtonStart_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(6, 46);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(65, 12);
            this.label1.TabIndex = 1;
            this.label1.Text = "* 輸入文件";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(6, 73);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(65, 12);
            this.label2.TabIndex = 2;
            this.label2.Text = "* 輸出文件";
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
            this.textBoxOut.Location = new System.Drawing.Point(77, 70);
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
            this.checkBoxInfo.Location = new System.Drawing.Point(20, 182);
            this.checkBoxInfo.Name = "checkBoxInfo";
            this.checkBoxInfo.Size = new System.Drawing.Size(90, 16);
            this.checkBoxInfo.TabIndex = 5;
            this.checkBoxInfo.Text = "新字體信息:";
            this.checkBoxInfo.UseVisualStyleBackColor = true;
            this.checkBoxInfo.CheckedChanged += new System.EventHandler(this.CheckBoxInfo_CheckedChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(4, 59);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(89, 12);
            this.label5.TabIndex = 1;
            this.label5.Text = "PostScript名稱";
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
            this.label4.Location = new System.Drawing.Point(28, 32);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(65, 12);
            this.label4.TabIndex = 1;
            this.label4.Text = "* 中文名稱";
            // 
            // textBoxChName
            // 
            this.textBoxChName.Location = new System.Drawing.Point(99, 29);
            this.textBoxChName.Name = "textBoxChName";
            this.textBoxChName.Size = new System.Drawing.Size(133, 21);
            this.textBoxChName.TabIndex = 7;
            this.textBoxChName.Text = "我的新字體";
            // 
            // textBoxPSName
            // 
            this.textBoxPSName.Location = new System.Drawing.Point(99, 56);
            this.textBoxPSName.Name = "textBoxPSName";
            this.textBoxPSName.Size = new System.Drawing.Size(133, 21);
            this.textBoxPSName.TabIndex = 8;
            this.textBoxPSName.Text = "MyNewFont";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(62, 86);
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
            this.label8.Location = new System.Drawing.Point(18, 100);
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
            this.comboBoxApp.Location = new System.Drawing.Point(77, 97);
            this.comboBoxApp.Name = "comboBoxApp";
            this.comboBoxApp.Size = new System.Drawing.Size(156, 20);
            this.comboBoxApp.TabIndex = 13;
            // 
            // checkBoxYitizi
            // 
            this.checkBoxYitizi.AutoSize = true;
            this.checkBoxYitizi.Checked = true;
            this.checkBoxYitizi.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxYitizi.Location = new System.Drawing.Point(22, 127);
            this.checkBoxYitizi.Name = "checkBoxYitizi";
            this.checkBoxYitizi.Size = new System.Drawing.Size(108, 16);
            this.checkBoxYitizi.TabIndex = 10;
            this.checkBoxYitizi.Text = "同時補全同義字";
            this.checkBoxYitizi.UseVisualStyleBackColor = true;
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.label5);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.textBoxName);
            this.panel1.Controls.Add(this.label6);
            this.panel1.Controls.Add(this.textBoxVersi);
            this.panel1.Controls.Add(this.textBoxPSName);
            this.panel1.Controls.Add(this.label4);
            this.panel1.Controls.Add(this.textBoxChName);
            this.panel1.Location = new System.Drawing.Point(111, 180);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(246, 112);
            this.panel1.TabIndex = 17;
            // 
            // panelMain
            // 
            this.panelMain.Controls.Add(this.comboBoxMulti);
            this.panelMain.Controls.Add(this.labelMilti);
            this.panelMain.Controls.Add(this.linkLabelOut);
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
            this.panelMain.Controls.Add(this.label1);
            this.panelMain.Controls.Add(this.textBoxIn);
            this.panelMain.Controls.Add(this.label2);
            this.panelMain.Location = new System.Drawing.Point(13, 13);
            this.panelMain.Name = "panelMain";
            this.panelMain.Size = new System.Drawing.Size(478, 297);
            this.panelMain.TabIndex = 18;
            // 
            // comboBoxMulti
            // 
            this.comboBoxMulti.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxMulti.FormattingEnabled = true;
            this.comboBoxMulti.Items.AddRange(new object[] {
            "不處理一對多",
            "使用單一常用字",
            "使用詞彙正確一簡對多繁"});
            this.comboBoxMulti.Location = new System.Drawing.Point(139, 150);
            this.comboBoxMulti.Name = "comboBoxMulti";
            this.comboBoxMulti.Size = new System.Drawing.Size(202, 20);
            this.comboBoxMulti.TabIndex = 20;
            // 
            // labelMilti
            // 
            this.labelMilti.AutoSize = true;
            this.labelMilti.Location = new System.Drawing.Point(18, 153);
            this.labelMilti.Name = "labelMilti";
            this.labelMilti.Size = new System.Drawing.Size(113, 12);
            this.labelMilti.TabIndex = 19;
            this.labelMilti.Text = "對簡繁一對多的處理";
            // 
            // linkLabelOut
            // 
            this.linkLabelOut.AutoSize = true;
            this.linkLabelOut.Location = new System.Drawing.Point(436, 73);
            this.linkLabelOut.Name = "linkLabelOut";
            this.linkLabelOut.Size = new System.Drawing.Size(29, 12);
            this.linkLabelOut.TabIndex = 18;
            this.linkLabelOut.TabStop = true;
            this.linkLabelOut.Text = "選擇";
            this.linkLabelOut.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabelOut_LinkClicked);
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
            // FormMain
            // 
            this.AcceptButton = this.buttonStart;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(506, 312);
            this.Controls.Add(this.panelMain);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "FormMain";
            this.ShowIcon = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = " 繁體字體製作";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FormMain_FormClosing);
            this.Load += new System.EventHandler(this.FormMain_Load);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.panelMain.ResumeLayout(false);
            this.panelMain.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
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
        private System.Windows.Forms.TextBox textBoxPSName;
        private System.Windows.Forms.TextBox textBoxChName;
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
    }
}

