# Discourse network analysis and party unity (dna-party)
The *dna-party* project explores the potential of discourse network analysis ([Leifeld 2016](https://books.google.co.uk/books/about/Policy_Debates_as_Dynamic_Networks.html?id=xKLuCwAAQBAJ&printsec=frontcover&source=kp_read_button&redir_esc=y#v=onepage&q&f=false)) for the study of party unity in the parliamentary context. Parliamentary debates have been coded manually using the [Discourse Network Analyzer](https://github.com/leifeld/dna). The raw data has then been exported, cleaned and prepared for analysis in Python.

The Python code allows us to:
* Explore the data
* Draw network graphs (including subtract networks)
* Compute the [Louvain modularity score](https://github.com/taynaud/python-louvain/)
* Compute the global clustering coefficient
* Compute the E-I index ([Krackhardt & Stern 1988](https://www.jstor.org/stable/pdf/2786835.pdf?casa_token=HfcKEMyPMy8AAAAA:5vpD6tmzxprEmioSZ5pLkzqE3loJyQhAcKfbbaUCEM8nB6Ow9-sJsi8LQeDTZzsgt1AXo2vDfciEL-JwFyjc2kiEMUPhGaLfkRBERkQjuYEuzffnEhibww))
* Compute a contestedness score for each concept

### Citation
If you use the dataset or code, please cite this paper:

[Bhattacharya, Caroline (2020), “Gatekeeping the Plenary Floor: Discourse Network Analysis as a Novel Approach to Party Control”, *Politics and Governance*, 8(2), 229-242.](https://www.cogitatiopress.com/politicsandgovernance/article/view/2611)

For comments or questions, please contact the author: https://blogs.helsinki.fi/czwerner/
