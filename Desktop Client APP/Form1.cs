using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        TcpClient client = new TcpClient();
        string server_addr = "127.0.0.1";

        public Form1()
        {
            client.Connect(server_addr, 2021);
            InitializeComponent();
            
        }

        private void button1_Click(object sender, EventArgs e)
        {

            //NetworkStream networkStream = client.GetStream();
            //networkStream.ReadTimeout = 2000;

            //var writer = new StreamWriter(networkStream);

            //string message = @"GET / HTTP/1.1
            //    Accept: text/html, charset=utf-8
            //    Accept-Language: en-US
            //    User-Agent: C# program
            //    Connection: close
            //    Host: 127.0.0.1" + "\r\n\r\n";

            //Console.WriteLine(message);

            //var reader = new StreamReader(networkStream, Encoding.UTF8);
            //byte[] bytes = Encoding.UTF8.GetBytes(message);

            //networkStream.Write(bytes, 0, bytes.Length);
            //Console.WriteLine(reader.ReadToEnd());

            int byteCount = Encoding.ASCII.GetByteCount(textBox1.Text);
            byte[] sendData = new byte[byteCount];
            byte[] bytes = Encoding.ASCII.GetBytes(textBox1.Text);
            NetworkStream stream = client.GetStream();
            stream.Write(bytes, 0, sendData.Length);
            
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            int byteCount = Encoding.ASCII.GetByteCount(textBox1.Text);
            byte[] sendData = new byte[byteCount];
            byte[] bytes = Encoding.ASCII.GetBytes(textBox1.Text);
            NetworkStream stream = client.GetStream();
            stream.Write(bytes, 0, sendData.Length);

            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            //
            client.Close();
        }
    }
}
