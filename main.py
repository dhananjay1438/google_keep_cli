# Modifying notes wouldn't work unless you don't add re._pattern_type = re.Pattern after importing
# re in __init__.py file of gkeepapi
import gkeepapi
import keyring
import getpass
import copy
import speech_recognition as sr

# Created empty to lists to store lists and notes respectively, which are already present
# in the google keep
gkeep_lists = []
gkeep_notes = []

# Creating a instance of google keep
keep = gkeepapi.Keep()

# Storing username and email
email = 'tempmail1438@gmail.com'
username = 'tempmail1438'

# Asking user for password as it is not a good practice to define password in variable

password = getpass.getpass(prompt='Please enter your password:')

if (keep.login(email, password)):
    print('Login successful!')
else:
    print('Incorrect Password!')
    exit(0)

# Syncing with google keep
keep.sync()

# Storing notes which are not archived currently present in the google keep in gnotes
found_gnotes = keep.find(archived=False)
found_labels = keep.labels()
gnotes = list()
for note in found_gnotes:
    gnotes.append(note)

# Creating dummy variable to check type of variables(items in gnotes) and
# add them to thier respective list
dummy_note = gkeepapi.node.Note()
for note in gnotes:

    if (type(note) == type(dummy_note)):
        gkeep_notes.append(note)
    else:
        gkeep_lists.append(note)

##########TODO Create a Notes class which has all the functionality###################


class NotesFunctionality():
    """
    Adds Functionality so notes can be created, deleted, undeleted, trashed, untrashed, undeleted,
    modified, labeled, unlabeled

    Attributes:

    notes (list of gkeepapi.node.Note): List of all notes(gkeepapi.node.Note) from google keep

    deleted_notes (list): List to store notes(gkeepapi.node.Note) which are deleted. This is used to
    recover notes after a note is deleted

    """
    notes = gkeep_notes
    deleted_notes = list()

    def __init__(self):
        pass

    def add_note(self, title, text):
        """
        Creates a note and adds it to google keep

        Parameters:

        title (str): Holds the title of note to be created

        text (str): Holds the content of the note to be created
        """
        self.notes.append(keep.createNote(title, text))

    def delete(self):
        """
        Deletes a note from google keep with specific numeric value assigned to it
        """
        # Running a loop through all the notes to assign a specific numeric value to it
        # So it can be deleted with that numeric value (or index)
        for i in range(0, len(self.notes)):
            print(
                f"Press {i} to delete note\nTITLE: {self.notes[i].title}\nText:{self.notes[i].text}")
        index_of_note_to_be_deleted = int(
            input("Enter a number to delete a note accordingly:"))

        # Title of the note to be deleted
        title_of_note_to_be_deleted = self.notes[index_of_note_to_be_deleted].title

        # Running through all the notes to find if any title of notes matches that of
        # note to be deleted
        for i in range(0, len(gnotes)):
            if (gnotes[i].title == title_of_note_to_be_deleted):
                # Add the deleted note to list so it can be used later to undelete note
                self.deleted_notes.append(gnotes[i])
                gnotes[i].delete()
        # Syncing to make changes visible
        keep.sync()
        print("Note Deleted!")

    def undelete(self, note):
        """
        Undeletes the deleted note from google keep

        Parameters:

        note (gkeepapi.node.Note): Note which is to be undeleted
        """
        # Creating a note which was deleted before and then adding it to global list of notes
        gnotes.append(keep.createNote(note.title, note.text))
        # Syncing to make changes visible
        keep.sync()

        #Addition feature just for ###########TESTING PURPOSE###############
        print("Items in gnotes")
        for item in gnotes:
            print(item)

    def modify_note(self):
        """
        Modifies a note which is nor archived neither trashed
        """
        for i in range(0, len(self.notes)):
            print(
                f"Press {i} to modify note\n Title: {self.notes[i].title}\nText: {self.notes[i].text}")

        index_of_note_to_be_modified = int(
            input("Enter a number to modify note accordingly:")
        )

        title_of_note_to_be_modified = self.notes[index_of_note_to_be_modified].title

        # Running a loop to check if title of note to be modified is same as any of the notes in
        # google keep if yes then modify text and title
        for i in range(0, len(gnotes)):
            if (title_of_note_to_be_modified == gnotes[i].title and type(gnotes[i]) == gkeepapi.node.Note):
                print("Note: Don't type anything if you want to keep it unchanged!")
                print(f"Previous title = {gnotes[i].title}")
                new_title = input("Enter new title:")
                print(f"Previous text = {gnotes[i].text}")
                new_text = input("Enter new text:")
                if (new_title != ""):
                    gnotes[i].title = new_title
                if (new_text != ""):
                    gnotes[i].text = new_text
                break
        keep.sync()
        print("Note modified")

    def add_label_to_note(self):
        """
        Adds label or labels to note
        """
        for i in range(0,len(self.notes)):
            print(f"Press {i} to add label to note \nTitle:{self.notes[i].title}\nText: {self.notes[i].text}")

        index_of_note_to_add_labels = int(
            input("Enter a number to add labels to a note accordingly:")
        )
        title_of_note_to_add_label = self.notes[index_of_note_to_add_labels].title
        note_to_add_label = gkeepapi.node.Note()
        for i in range(0, len(gnotes)):
            if (gnotes[i].title == title_of_note_to_add_label):
                note_to_add_label = gnotes[i]

        labels = input("Enter label or labels to assign it to note:")
        labels = labels.split(" ")
        for label in labels:
                new_label = keep.createLabel(label)
                note_to_add_label.labels.add(new_label)


        keep.sync()


i = NotesFunctionality()
i.add_label_to_note()
print(found_labels)
# i.modify_note()
# i.delete()
# i.undelete(i.deleted_notes[0])

#########TODO Create a Lists class which has all the functionality####################
