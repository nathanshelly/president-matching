# Which Professor Are You?
Built by Nathan Shelly and Sasha Weiss, for EECS 352 at Northwestern University, WQ17.

## Voice Matching
Which Professor Are You investigates voice-similarity matching. Specifically, we investigated various audio features that could be used to match a speaker to others they "sound the most like". As an application of this project, our project records a speaker, and presents them with the Northwestern EECS professor their voice most closely resembles.

Our implementation relies on [MFCCs][4], which it uses as features for training and testing using a [GMM classifier][5]. You can read our report [here][6].

## Dependencies
Most dependencies are reflected in `requirements.txt`. To install using Pip, run `pip install -r requirements.txt`.

This project uses Python 2.7.

### Essentia
This project also depends on [essentia][1], which is not reflected in requirements.txt.

#### Essentia and Virtualenv
To run this project in a [virtual environment][2], it is necessary to build/install essentia to your machine, and copy the package into your `<venv>/lib/python2.7/site-packages/` directory. See [this link][3] for help.

[1]: http://essentia.upf.edu/
[2]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[3]: https://github.com/MTG/essentia/issues/553
[4]: https://www.wikiwand.com/en/Mel-frequency_cepstrum
[5]: http://scikit-learn.org/stable/modules/mixture.html
[6]: https://docs.google.com/presentation/d/1xWapGB6mQnUaBJ-nfJyglCsV5nFxxiZ-G2ivald6820/edit?usp=sharing
