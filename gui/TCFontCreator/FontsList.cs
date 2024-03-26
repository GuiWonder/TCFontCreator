using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TCFontCreator
{
    public partial class FontsList : Form
    {
        readonly OpenFileDialog openFileDialog = new OpenFileDialog();
        readonly FormMain f1;
        public FontsList(FormMain form1)
        {
            InitializeComponent();
            f1 = form1;
            buttonAdd.Click += ButtonAdd_Click;
            buttonRemove.Click += ButtonRemove_Click;
            buttonInsert.Click += ButtonInsert_Click;
            buttonUp.Click += ButtonUp_Click;
            buttonDown.Click += ButtonDown_Click;
            buttonClear.Click += ButtonClear_Click;
            listBox.DragEnter += ListBox_DragEnter;
            listBox.DragDrop += ListBox_DragDrop;

            openFileDialog.Multiselect = true;
            openFileDialog.Filter = f1.listMsg[8];
            buttonOK.Click += ButtonOK_Click;
            LastFontsToList();

        }

        private void LastFontsToList()
        {
            if (f1.addfonts.Count>0)
            {
                foreach (var item in f1.addfonts)
                {
                    listBox.Items.Add(item);
                }
            }
        }

        private void ButtonOK_Click(object sender, EventArgs e)
        {
            f1.addfonts.Clear();
            foreach (var item in listBox.Items)
            {
                f1.addfonts.Add((string)item);
            }
        }
        #region Button
        private void ButtonAdd_Click(object sender, EventArgs e) => AddfileToList();
        private void ButtonRemove_Click(object sender, EventArgs e) => RemoveSelected();
        private void ButtonUp_Click(object sender, EventArgs e) => UpfileToList();
        private void ButtonDown_Click(object sender, EventArgs e) => DownfileToList();
        private void ButtonInsert_Click(object sender, EventArgs e) => InsertfileToList();
        private void ButtonClear_Click(object sender, EventArgs e) => listBox.Items.Clear();

        #endregion

        #region ListView

        private void ListBox_DragDrop(object sender, DragEventArgs e)
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

        private void ListBox_DragEnter(object sender, DragEventArgs e) => e.Effect = e.Data.GetDataPresent(DataFormats.FileDrop) ? DragDropEffects.All : DragDropEffects.None;

        #endregion

        #region Main


        private void AddfileToList()
        {
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                foreach (var item in openFileDialog.FileNames)
                {
                    listBox.Items.Add(item);
                }
            }
        }
        private void UpfileToList()
        {
            int i = listBox.SelectedIndex;
            if (i < 0)
            {
                return;
            }
            if (i > 0)
            {
                (listBox.Items[i], listBox.Items[i - 1]) = (listBox.Items[i - 1], listBox.Items[i]);
                listBox.SelectedIndex = i - 1;
            }

        }
        private void DownfileToList()
        {
            int i = listBox.SelectedIndex;
            if (i < 0)
            {
                return;
            }
            if (i < listBox.Items.Count - 1)
            {
                (listBox.Items[i + 1], listBox.Items[i]) = (listBox.Items[i], listBox.Items[i + 1]);
                listBox.SelectedIndex = i + 1;
            }

        }
        private void InsertfileToList()
        {
            int i = listBox.SelectedIndex;
            if (i < 0)
            {
                return;
            }
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                listBox.Items.Insert(i, openFileDialog.FileName);
            }

        }

        private void RemoveSelected()
        {
            int index = listBox.SelectedIndex;
            if (index < 0)
            {
                return;
            }
            listBox.Items.RemoveAt(index);
            if (index >= listBox.Items.Count - 1 && index > 0)
            {
                listBox.SelectedIndex = listBox.Items.Count - 1;
            }
            else if (index == 0 && listBox.Items.Count > 0)
            {
                listBox.SelectedIndex = 0;
            }
            else
            {
                listBox.SelectedIndex = index - 1;
            }
        }

        #endregion
    }
}
