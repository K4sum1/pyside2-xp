
#############################################################################
##
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>
## Copyright (C) 2011 Arun Srinivasan <rulfzid@gmail.com>
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

from PySide2.QtWidgets import (QWidget)
from PySide2.QtGui import (QPainter)
from PySide2.QtCore import Signal

from starrating import StarRating

class StarEditor(QWidget):
    """ The custom editor for editing StarRatings. """

    # A signal to tell the delegate when we've finished editing.
    editingFinished = Signal()

    def __init__(self, parent=None):
        """ Initialize the editor object, making sure we can watch mouse
            events.
        """
        super(StarEditor, self).__init__(parent)

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.starRating = StarRating()

    def sizeHint(self):
        """ Tell the caller how big we are. """
        return self.starRating.sizeHint()

    def paintEvent(self, event):
        """ Paint the editor, offloading the work to the StarRating class. """
        painter = QPainter(self)
        self.starRating.paint(painter, self.rect(), self.palette(), isEditable=True)

    def mouseMoveEvent(self, event):
        """ As the mouse moves inside the editor, track the position and
            update the editor to display as many stars as necessary.
        """
        star = self.starAtPosition(event.x())

        if (star != self.starRating.starCount) and (star != -1):
            self.starRating.starCount = star
            self.update()

    def mouseReleaseEvent(self, event):
        """ Once the user has clicked his/her chosen star rating, tell the
            delegate we're done editing.
        """
        self.editingFinished.emit()

    def starAtPosition(self, x):
        """ Calculate which star the user's mouse cursor is currently
            hovering over.
        """
        star = (x / (self.starRating.sizeHint().width() /
                     self.starRating.maxStarCount)) + 1
        if (star <= 0) or (star > self.starRating.maxStarCount):
            return -1

        return star
