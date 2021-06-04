FROM greyltc/archlinux-aur
RUN pacman -Syy --noconfirm python-pyqt5 python-numpy python-pip ffmpeg sox patchelf
RUN sudo -u ab -D~ bash -c 'yay -Syu --removemake --needed --noprogressbar --noconfirm ffmpeg-normalize'
RUN pip install wheel pillow cx_Freeze mp3chaps tinytag pydub
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp
RUN git clone https://github.com/trevligmjukvara/audio-visualizer-python && cd audio-visualizer-python
RUN mkdir /tm /tm/Recordings
RUN mkdir -p /usr/share/fonts/ttf/SulphurPoint
ADD SulphurPoint /usr/share/fonts/ttf/SulphurPoint
RUN echo -e '#!/usr/sbin/bash\npython /audio-visualizer-python/main.py "$@"' > /usr/sbin/audio-visualizer-python
RUN chmod +x /usr/sbin/audio-visualizer-python
VOLUME ["/tm"]
WORKDIR /tm/Recordings
ENTRYPOINT ["bash", "./produce-episode.sh"]
