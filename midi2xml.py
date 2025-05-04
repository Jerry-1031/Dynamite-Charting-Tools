import mido
import xml.etree.ElementTree as et

name = 'name'
diff = 'G'
mid = mido.MidiFile(name + '.mid')
time = 0
bpm = 120.0
mn, mx = 35, 95
mnnote, mxnote = 128, 0
cnt = 0
tempo = mido.bpm2tempo(bpm)
meter = 4.0
offset = 0.0
width = 0.5

print('Welcome to midi2xml!')
print('Midi Name:', name)
print('BPM:', bpm)
print('Offset:', offset)
print('Note Width:', width)

def note2pos(note):
    return (note - mn) / (mx - mn) * 5

print('Start Converting')
str_width = str(width)
root = et.Element('CMap')
m_barPerMin = et.SubElement(root, 'm_barPerMin')
m_barPerMin.text = "{:.6f}".format(bpm / 4)
m_leftRegion = et.SubElement(root, 'm_leftRegion')
m_leftRegion.text = 'PAD'
m_mapID = et.SubElement(root, 'm_mapID')
m_mapID.text = '_map_' + name + '_' + diff
m_notes0 = et.SubElement(root, 'm_notes')
m_notes00 = et.SubElement(m_notes0, 'm_notes')

for msg in mid.play():
    time += msg.time * 1000000 / meter / tempo
    if msg.type == 'note_on' and msg.velocity != 0:
        Note = et.SubElement(m_notes00, 'CMapNoteAsset')
        m_type = et.SubElement(Note, 'm_type')
        m_type.text = 'NORMAL'
        m_width = et.SubElement(Note, 'm_width')
        m_width.text = str_width
        m_id = et.SubElement(Note, 'm_id')
        m_id.text = str(cnt)
        m_position = et.SubElement(Note, 'm_position')
        m_position.text = "{:.6f}".format(note2pos(msg.note))
        m_subId = et.SubElement(Note, 'm_subId')
        m_subId.text = '-1'
        m_time = et.SubElement(Note, 'm_time')
        m_time.text = "{:.6f}".format(time)
        print([msg.note, "{:.6f}".format(time)])
        cnt += 1
        if msg.note < mnnote:
            mnnote = msg.note
        if msg.note > mxnote:
            mxnote = msg.note

m_notesLeft = et.SubElement(root, 'm_notesLeft')
m_notesLeft0 = et.SubElement(m_notesLeft, 'm_notes')
m_notesRight = et.SubElement(root, 'm_notesRight')
m_notesRight0 = et.SubElement(m_notesRight, 'm_notes')
m_path = et.SubElement(root, 'm_path')
m_path.text = name
m_rightRegion = et.SubElement(root, 'm_rightRegion')
m_rightRegion.text = 'PAD'
m_timeOffset = et.SubElement(root, 'm_timeOffset')
m_timeOffset.text = "{:.6f}".format(offset)
print('Total Notes Count:', cnt)
print('Lowest Note:', mnnote, note2pos(mnnote))
print('Highest Note:', mxnote, note2pos(mxnote))

with open(name + '.xml', 'w') as f:
    s = et.tostring(root, short_empty_elements=False).decode()
    print('Convert Successfully!')
    f.write('<?xml version="1.0"?>\n')
    f.write(s.replace('<CMap>', '<CMap xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">', 1))
    print('Output File Name:', name + '.xml')
