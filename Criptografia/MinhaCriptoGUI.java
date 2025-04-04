package ifprseg;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class MinhaCriptoGUI extends JFrame {
    private JTextField inputText, outputText, keyField;
    private JButton encryptButton, decryptButton;
    
    private static final int KEY = 4;

    public MinhaCriptoGUI() {
        setTitle("Cifra de Misteriosa L6");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(4, 2, 5, 5));

        JLabel inputLabel = new JLabel("Texto:");
        inputText = new JTextField(20);
      
        JLabel outputLabel = new JLabel("Resultado:");
        outputText = new JTextField(20);
        outputText.setEditable(false);

        encryptButton = new JButton("Criptografar");
        encryptButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                encryptText();
            }
        });

        decryptButton = new JButton("Descriptografar");
        decryptButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                decryptText();
            }
        });

        panel.add(inputLabel);
        panel.add(inputText);       
        panel.add(outputLabel);
        panel.add(outputText);
        panel.add(encryptButton);
        panel.add(decryptButton);

        add(panel, BorderLayout.CENTER);
        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    private void encryptText() {
        String text = inputText.getText();        
        String encryptedText = caesarCipher(text, KEY);
        outputText.setText(encryptedText);
    }

    private void decryptText() {
        String text = inputText.getText();        
        String decryptedText = caesarCipher(text, -KEY);
        outputText.setText(decryptedText);
    }

    private String caesarCipher(String text, int key) {
        StringBuilder result = new StringBuilder();

        for (char ch : text.toCharArray()) {
        	
        	char letter = ch;		    
		    
		    if (ch >= 'a' && ch <= 'z') {		    	
			    letter = (char)(((ch-'a')+key+26)%26 + 'a');		
			}else if(ch >= 'A' && ch <= 'Z') {		    	
			    letter = (char)(((ch-'A')+key+26)%26 + 'A');		
			}		    
            result.append(letter);            
        }

        return result.toString();
    }
    
    /*
    private static final char[] SUBSTITUTION_KEY = {
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'
        };
    private String cifraDeSubstituicao(String texto) {
        StringBuilder resultado = new StringBuilder();
        for (char c : texto.toCharArray()) {
            if (Character.isLetter(c)) {
                int index = (c - 'a') % 26;
                resultado.append(SUBSTITUTION_KEY[index]);
            } else {
                resultado.append(c);
            }
        }
        return resultado.toString();
    }

    private String decifraDeSubstituicao(String texto) {
        StringBuilder resultado = new StringBuilder();
        for (char c : texto.toCharArray()) {
            if (Character.isLetter(c)) {
                int index = new String(SUBSTITUTION_KEY).indexOf(c);
                resultado.append((char) ('a' + index));
            } else {
                resultado.append(c);
            }
        }
        return resultado.toString();
    }
    */
    
    
 // Vetor de substituição
    private static final char[] SUBSTITUTION_KEY = {
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'
    };

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new MinhaCriptoGUI();
            }
        });
    }
}
