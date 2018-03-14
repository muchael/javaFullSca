package {package};

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;

import org.directwebremoting.annotations.DataTransferObject;
import org.hibernate.envers.Audited;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@Entity
@Audited
@EqualsAndHashCode(callSuper = true)
@DataTransferObject(javascript = "{entityName}")
@Table(name = "{tableName}")
@SequenceIdName("SQ_{tableName}_PK")
public class {entityName} extends AbstractEntity 
{
	/*-------------------------------------------------------------------
	 *				 		     ATTRIBUTES
	 *-------------------------------------------------------------------*/
    
    // {attributes}

	/*-------------------------------------------------------------------
	 * 		 					CONSTRUCTORS
	 *-------------------------------------------------------------------*/
	
	/**
	 * 
	 */
	public {entityName}()
	{
		super();
	}

	/**
	 * @param id
	 */
	public {entityName}( Long id )
	{
		super( id );
	}
}
